/**
 * Tests end-to-end pour la connexion
 */
describe('Login Flow', () => {
  beforeEach(() => {
    cy.visit('/login')
  })

  it('should display login form', () => {
    cy.get('form').should('be.visible')
    cy.get('input[name="username"]').should('be.visible')
    cy.get('input[name="password"]').should('be.visible')
    cy.get('button[type="submit"]').should('be.visible')
  })

  it('should show validation errors for empty fields', () => {
    cy.get('button[type="submit"]').click()
    cy.get('.form-error').should('be.visible')
  })

  it('should login with valid credentials', () => {
    cy.get('input[name="username"]').type('admin')
    cy.get('input[name="password"]').type('admin123')
    cy.get('button[type="submit"]').click()
    
    cy.url().should('include', '/dashboard')
    cy.get('[data-testid="dashboard"]').should('be.visible')
  })

  it('should show error for invalid credentials', () => {
    cy.get('input[name="username"]').type('invalid')
    cy.get('input[name="password"]').type('invalid')
    cy.get('button[type="submit"]').click()
    
    cy.get('.toast-error').should('be.visible')
  })

  it('should redirect to dashboard if already logged in', () => {
    // Simuler une session active
    cy.window().then((win) => {
      win.localStorage.setItem('token', 'mock-token')
    })
    
    cy.visit('/login')
    cy.url().should('include', '/dashboard')
  })
})
