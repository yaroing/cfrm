/**
 * Tests mobile end-to-end
 */
describe('Mobile Tests', () => {
  beforeEach(() => {
    // Simuler une session active
    cy.window().then((win) => {
      win.localStorage.setItem('token', 'mock-token')
    })
  })

  it('should work on iPhone', () => {
    cy.viewport(375, 667) // iPhone SE
    cy.visit('/dashboard')
    
    cy.get('[data-testid="mobile-menu"]').should('be.visible')
    cy.get('[data-testid="dashboard"]').should('be.visible')
  })

  it('should work on iPad', () => {
    cy.viewport(768, 1024) // iPad
    cy.visit('/dashboard')
    
    cy.get('[data-testid="dashboard"]').should('be.visible')
    cy.get('[data-testid="sidebar"]').should('be.visible')
  })

  it('should work on Android', () => {
    cy.viewport(360, 640) // Android
    cy.visit('/dashboard')
    
    cy.get('[data-testid="mobile-menu"]').should('be.visible')
    cy.get('[data-testid="dashboard"]').should('be.visible')
  })

  it('should have touch-friendly buttons', () => {
    cy.viewport(375, 667)
    cy.visit('/dashboard')
    
    // Vérifier que les boutons sont assez grands pour le tactile
    cy.get('button').each(($button) => {
      cy.wrap($button).should('have.css', 'min-height', '44px')
      cy.wrap($button).should('have.css', 'min-width', '44px')
    })
  })

  it('should have proper mobile navigation', () => {
    cy.viewport(375, 667)
    cy.visit('/dashboard')
    
    // Vérifier le menu mobile
    cy.get('[data-testid="mobile-menu-button"]').click()
    cy.get('[data-testid="mobile-menu"]').should('be.visible')
    
    // Vérifier la navigation
    cy.get('[data-testid="mobile-menu"] a').should('have.length.greaterThan', 0)
  })

  it('should handle mobile forms', () => {
    cy.viewport(375, 667)
    cy.visit('/login')
    
    // Vérifier que les champs de formulaire sont adaptés au mobile
    cy.get('input[name="username"]').should('have.attr', 'type', 'text')
    cy.get('input[name="password"]').should('have.attr', 'type', 'password')
    
    // Vérifier que le clavier virtuel s'ouvre correctement
    cy.get('input[name="username"]').focus()
    cy.focused().should('be.visible')
  })

  it('should handle mobile tables', () => {
    cy.viewport(375, 667)
    cy.visit('/tickets')
    
    // Vérifier que le tableau est adapté au mobile
    cy.get('[data-testid="tickets-table"]').should('be.visible')
    cy.get('[data-testid="mobile-table-view"]').should('be.visible')
  })

  it('should handle mobile modals', () => {
    cy.viewport(375, 667)
    cy.visit('/tickets')
    
    cy.get('[data-testid="create-ticket-button"]').click()
    
    // Vérifier que le modal est adapté au mobile
    cy.get('[data-testid="ticket-form"]').should('be.visible')
    cy.get('[data-testid="mobile-modal"]').should('be.visible')
  })

  it('should handle mobile scrolling', () => {
    cy.viewport(375, 667)
    cy.visit('/tickets')
    
    // Vérifier que le défilement fonctionne sur mobile
    cy.get('[data-testid="tickets-table"]').scrollTo('bottom')
    cy.get('[data-testid="tickets-table"]').should('be.visible')
  })

  it('should handle mobile gestures', () => {
    cy.viewport(375, 667)
    cy.visit('/dashboard')
    
    // Vérifier que les gestes tactiles fonctionnent
    cy.get('[data-testid="dashboard"]').swipe('left')
    cy.get('[data-testid="dashboard"]').swipe('right')
  })

  it('should handle mobile orientation changes', () => {
    cy.viewport(375, 667)
    cy.visit('/dashboard')
    
    // Vérifier le mode portrait
    cy.get('[data-testid="dashboard"]').should('be.visible')
    
    // Changer en mode paysage
    cy.viewport(667, 375)
    cy.get('[data-testid="dashboard"]').should('be.visible')
    
    // Revenir en mode portrait
    cy.viewport(375, 667)
    cy.get('[data-testid="dashboard"]').should('be.visible')
  })

  it('should handle mobile network conditions', () => {
    cy.viewport(375, 667)
    
    // Simuler une connexion lente
    cy.intercept('GET', '/api/v1/tickets/tickets/', (req) => {
      req.reply((res) => {
        res.delay(2000)
        return res
      })
    }).as('getTicketsSlow')
    
    cy.visit('/tickets')
    
    // Vérifier que l'état de chargement est affiché
    cy.get('[data-testid="loading-spinner"]').should('be.visible')
    
    cy.wait('@getTicketsSlow')
    cy.get('[data-testid="tickets-table"]').should('be.visible')
  })

  it('should handle mobile keyboard', () => {
    cy.viewport(375, 667)
    cy.visit('/login')
    
    // Vérifier que le clavier virtuel s'ouvre
    cy.get('input[name="username"]').focus()
    cy.focused().should('be.visible')
    
    // Vérifier que le clavier se ferme
    cy.get('input[name="username"]').blur()
    cy.focused().should('not.exist')
  })

  it('should handle mobile alerts', () => {
    cy.viewport(375, 667)
    cy.visit('/login')
    
    // Tenter une connexion invalide
    cy.get('input[name="username"]').type('invalid')
    cy.get('input[name="password"]').type('invalid')
    cy.get('button[type="submit"]').click()
    
    // Vérifier que l'alerte est adaptée au mobile
    cy.get('.toast-error').should('be.visible')
    cy.get('.toast-error').should('have.css', 'position', 'fixed')
  })

  it('should handle mobile search', () => {
    cy.viewport(375, 667)
    cy.visit('/tickets')
    
    // Vérifier que la recherche est adaptée au mobile
    cy.get('[data-testid="search-input"]').should('be.visible')
    cy.get('[data-testid="search-input"]').should('have.attr', 'placeholder')
    
    // Vérifier que la recherche fonctionne
    cy.get('[data-testid="search-input"]').type('test')
    cy.get('[data-testid="search-button"]').click()
    
    cy.get('[data-testid="tickets-table"]').should('be.visible')
  })

  it('should handle mobile filters', () => {
    cy.viewport(375, 667)
    cy.visit('/tickets')
    
    // Vérifier que les filtres sont adaptés au mobile
    cy.get('[data-testid="filters-button"]').click()
    cy.get('[data-testid="mobile-filters"]').should('be.visible')
    
    // Vérifier que les filtres fonctionnent
    cy.get('[data-testid="status-filter"]').select('Ouvert')
    cy.get('[data-testid="apply-filters"]').click()
    
    cy.get('[data-testid="tickets-table"]').should('be.visible')
  })

  it('should handle mobile pagination', () => {
    cy.viewport(375, 667)
    cy.visit('/tickets')
    
    // Vérifier que la pagination est adaptée au mobile
    cy.get('[data-testid="pagination"]').should('be.visible')
    cy.get('[data-testid="mobile-pagination"]').should('be.visible')
    
    // Vérifier que la pagination fonctionne
    cy.get('[data-testid="next-page"]').click()
    cy.get('[data-testid="tickets-table"]').should('be.visible')
  })

  it('should handle mobile modals', () => {
    cy.viewport(375, 667)
    cy.visit('/tickets')
    
    cy.get('[data-testid="create-ticket-button"]').click()
    
    // Vérifier que le modal est adapté au mobile
    cy.get('[data-testid="ticket-form"]').should('be.visible')
    cy.get('[data-testid="mobile-modal"]').should('be.visible')
    
    // Vérifier que le modal se ferme
    cy.get('[data-testid="close-modal"]').click()
    cy.get('[data-testid="ticket-form"]').should('not.exist')
  })

  it('should handle mobile notifications', () => {
    cy.viewport(375, 667)
    cy.visit('/dashboard')
    
    // Vérifier que les notifications sont adaptées au mobile
    cy.get('[data-testid="notifications"]').should('be.visible')
    cy.get('[data-testid="mobile-notifications"]').should('be.visible')
  })

  it('should handle mobile charts', () => {
    cy.viewport(375, 667)
    cy.visit('/dashboard')
    
    // Vérifier que les graphiques sont adaptés au mobile
    cy.get('[data-testid="charts"]').should('be.visible')
    cy.get('[data-testid="mobile-charts"]').should('be.visible')
  })

  it('should handle mobile analytics', () => {
    cy.viewport(375, 667)
    cy.visit('/analytics')
    
    // Vérifier que les analytics sont adaptés au mobile
    cy.get('[data-testid="analytics"]').should('be.visible')
    cy.get('[data-testid="mobile-analytics"]').should('be.visible')
  })
})