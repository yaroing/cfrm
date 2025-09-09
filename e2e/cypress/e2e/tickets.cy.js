/**
 * Tests end-to-end pour la gestion des tickets
 */
describe('Tickets Management', () => {
  beforeEach(() => {
    // Simuler une session active
    cy.window().then((win) => {
      win.localStorage.setItem('token', 'mock-token')
    })
    
    cy.visit('/tickets')
  })

  it('should display tickets list', () => {
    cy.get('[data-testid="tickets-table"]').should('be.visible')
    cy.get('[data-testid="tickets-filters"]').should('be.visible')
  })

  it('should filter tickets by status', () => {
    cy.get('[data-testid="status-filter"]').select('Ouvert')
    cy.get('[data-testid="apply-filters"]').click()
    
    cy.get('[data-testid="tickets-table"] tbody tr').should('have.length.greaterThan', 0)
  })

  it('should search tickets', () => {
    cy.get('[data-testid="search-input"]').type('test')
    cy.get('[data-testid="search-button"]').click()
    
    cy.get('[data-testid="tickets-table"] tbody tr').should('have.length.greaterThan', 0)
  })

  it('should create new ticket', () => {
    cy.get('[data-testid="create-ticket-button"]').click()
    
    cy.get('[data-testid="ticket-form"]').should('be.visible')
    cy.get('input[name="title"]').type('Test Ticket')
    cy.get('textarea[name="content"]').type('Test content')
    cy.get('select[name="category"]').select('1')
    cy.get('select[name="priority"]').select('3')
    cy.get('select[name="channel"]').select('4')
    
    cy.get('[data-testid="submit-ticket"]').click()
    
    cy.get('.toast-success').should('be.visible')
    cy.url().should('include', '/tickets')
  })

  it('should view ticket details', () => {
    cy.get('[data-testid="tickets-table"] tbody tr').first().click()
    
    cy.get('[data-testid="ticket-details"]').should('be.visible')
    cy.get('[data-testid="ticket-title"]').should('be.visible')
    cy.get('[data-testid="ticket-content"]').should('be.visible')
  })

  it('should assign ticket', () => {
    cy.get('[data-testid="tickets-table"] tbody tr').first().click()
    
    cy.get('[data-testid="assign-ticket"]').click()
    cy.get('[data-testid="assignee-select"]').select('1')
    cy.get('[data-testid="confirm-assign"]').click()
    
    cy.get('.toast-success').should('be.visible')
  })

  it('should close ticket', () => {
    cy.get('[data-testid="tickets-table"] tbody tr').first().click()
    
    cy.get('[data-testid="close-ticket"]').click()
    cy.get('[data-testid="confirm-close"]').click()
    
    cy.get('.toast-success').should('be.visible')
  })

  it('should add response to ticket', () => {
    cy.get('[data-testid="tickets-table"] tbody tr').first().click()
    
    cy.get('[data-testid="add-response"]').click()
    cy.get('[data-testid="response-content"]').type('This is a response')
    cy.get('[data-testid="submit-response"]').click()
    
    cy.get('.toast-success').should('be.visible')
  })
})
