/**
 * Tests end-to-end pour le tableau de bord
 */
describe('Dashboard', () => {
  beforeEach(() => {
    // Simuler une session active
    cy.window().then((win) => {
      win.localStorage.setItem('token', 'mock-token')
    })
    
    cy.visit('/dashboard')
  })

  it('should display dashboard elements', () => {
    cy.get('[data-testid="dashboard-stats"]').should('be.visible')
    cy.get('[data-testid="recent-tickets"]').should('be.visible')
    cy.get('[data-testid="quick-actions"]').should('be.visible')
    cy.get('[data-testid="charts"]').should('be.visible')
  })

  it('should show user information', () => {
    cy.get('[data-testid="user-menu"]').should('be.visible')
    cy.get('[data-testid="user-name"]').should('contain', 'Admin')
  })

  it('should navigate to tickets page', () => {
    cy.get('[data-testid="tickets-link"]').click()
    cy.url().should('include', '/tickets')
  })

  it('should navigate to analytics page', () => {
    cy.get('[data-testid="analytics-link"]').click()
    cy.url().should('include', '/analytics')
  })

  it('should logout successfully', () => {
    cy.get('[data-testid="user-menu"]').click()
    cy.get('[data-testid="logout-button"]').click()
    
    cy.url().should('include', '/login')
    cy.window().then((win) => {
      expect(win.localStorage.getItem('token')).to.be.null
    })
  })
})
