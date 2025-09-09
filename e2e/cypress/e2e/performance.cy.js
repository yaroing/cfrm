/**
 * Tests de performance end-to-end
 */
describe('Performance Tests', () => {
  beforeEach(() => {
    // Simuler une session active
    cy.window().then((win) => {
      win.localStorage.setItem('token', 'mock-token')
    })
  })

  it('should load dashboard quickly', () => {
    const startTime = Date.now()
    
    cy.visit('/dashboard')
    cy.get('[data-testid="dashboard"]').should('be.visible')
    
    const loadTime = Date.now() - startTime
    expect(loadTime).to.be.lessThan(3000) // Moins de 3 secondes
  })

  it('should load tickets list quickly', () => {
    const startTime = Date.now()
    
    cy.visit('/tickets')
    cy.get('[data-testid="tickets-table"]').should('be.visible')
    
    const loadTime = Date.now() - startTime
    expect(loadTime).to.be.lessThan(2000) // Moins de 2 secondes
  })

  it('should handle large datasets efficiently', () => {
    // Simuler un grand nombre de tickets
    cy.intercept('GET', '/api/v1/tickets/tickets/', {
      fixture: 'large-tickets-list.json'
    }).as('getTickets')
    
    cy.visit('/tickets')
    cy.wait('@getTickets')
    
    cy.get('[data-testid="tickets-table"] tbody tr').should('have.length', 100)
    
    // Vérifier que la pagination est présente
    cy.get('[data-testid="pagination"]').should('be.visible')
  })

  it('should have good Core Web Vitals', () => {
    cy.visit('/dashboard')
    
    // Vérifier les métriques de performance
    cy.window().then((win) => {
      const performance = win.performance
      const navigation = performance.getEntriesByType('navigation')[0]
      
      // First Contentful Paint
      const fcp = performance.getEntriesByName('first-contentful-paint')[0]
      expect(fcp.startTime).to.be.lessThan(2000)
      
      // Largest Contentful Paint
      const lcp = performance.getEntriesByName('largest-contentful-paint')[0]
      expect(lcp.startTime).to.be.lessThan(4000)
      
      // Cumulative Layout Shift
      const cls = performance.getEntriesByType('layout-shift')
      const totalCLS = cls.reduce((sum, entry) => sum + entry.value, 0)
      expect(totalCLS).to.be.lessThan(0.1)
    })
  })

  it('should handle concurrent requests efficiently', () => {
    // Simuler plusieurs requêtes simultanées
    cy.intercept('GET', '/api/v1/tickets/tickets/dashboard_stats/').as('getStats')
    cy.intercept('GET', '/api/v1/tickets/tickets/').as('getTickets')
    cy.intercept('GET', '/api/v1/channels/channels/').as('getChannels')
    
    cy.visit('/dashboard')
    
    cy.wait(['@getStats', '@getTickets', '@getChannels'])
    
    // Vérifier que toutes les requêtes sont terminées
    cy.get('[data-testid="dashboard-stats"]').should('be.visible')
    cy.get('[data-testid="recent-tickets"]').should('be.visible')
  })

  it('should have efficient memory usage', () => {
    cy.visit('/dashboard')
    
    cy.window().then((win) => {
      const initialMemory = win.performance.memory?.usedJSHeapSize || 0
      
      // Naviguer entre plusieurs pages
      cy.get('[data-testid="tickets-link"]').click()
      cy.get('[data-testid="analytics-link"]').click()
      cy.get('[data-testid="dashboard-link"]').click()
      
      // Vérifier que la mémoire n'a pas augmenté de manière significative
      const finalMemory = win.performance.memory?.usedJSHeapSize || 0
      const memoryIncrease = finalMemory - initialMemory
      
      expect(memoryIncrease).to.be.lessThan(10 * 1024 * 1024) // Moins de 10MB
    })
  })

  it('should handle slow network conditions', () => {
    // Simuler une connexion lente
    cy.intercept('GET', '/api/v1/tickets/tickets/', (req) => {
      req.reply((res) => {
        res.delay(2000) // 2 secondes de délai
        return res
      })
    }).as('getTicketsSlow')
    
    cy.visit('/tickets')
    
    // Vérifier que l'état de chargement est affiché
    cy.get('[data-testid="loading-spinner"]').should('be.visible')
    
    cy.wait('@getTicketsSlow')
    cy.get('[data-testid="tickets-table"]').should('be.visible')
  })

  it('should have efficient search performance', () => {
    cy.visit('/tickets')
    
    const startTime = Date.now()
    
    cy.get('[data-testid="search-input"]').type('test')
    cy.get('[data-testid="search-button"]').click()
    
    cy.get('[data-testid="tickets-table"] tbody tr').should('have.length.greaterThan', 0)
    
    const searchTime = Date.now() - startTime
    expect(searchTime).to.be.lessThan(1000) // Moins d'1 seconde
  })

  it('should handle form submissions efficiently', () => {
    cy.visit('/tickets')
    
    cy.get('[data-testid="create-ticket-button"]').click()
    
    const startTime = Date.now()
    
    cy.get('input[name="title"]').type('Performance Test Ticket')
    cy.get('textarea[name="content"]').type('Testing form submission performance')
    cy.get('select[name="category"]').select('1')
    cy.get('select[name="priority"]').select('3')
    cy.get('select[name="channel"]').select('4')
    
    cy.get('[data-testid="submit-ticket"]').click()
    
    cy.get('.toast-success').should('be.visible')
    
    const submitTime = Date.now() - startTime
    expect(submitTime).to.be.lessThan(2000) // Moins de 2 secondes
  })
})