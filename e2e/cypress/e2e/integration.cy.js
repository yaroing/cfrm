/**
 * Tests d'intégration end-to-end
 */
describe('Integration Tests', () => {
  beforeEach(() => {
    // Simuler une session active
    cy.window().then((win) => {
      win.localStorage.setItem('token', 'mock-token')
    })
  })

  it('should complete full ticket workflow', () => {
    // 1. Créer un ticket
    cy.visit('/tickets')
    cy.get('[data-testid="create-ticket-button"]').click()
    
    cy.get('input[name="title"]').type('Integration Test Ticket')
    cy.get('textarea[name="content"]').type('This is a test ticket for integration testing')
    cy.get('select[name="category"]').select('1')
    cy.get('select[name="priority"]').select('3')
    cy.get('select[name="channel"]').select('4')
    
    cy.get('[data-testid="submit-ticket"]').click()
    cy.get('.toast-success').should('be.visible')
    
    // 2. Vérifier que le ticket est créé
    cy.get('[data-testid="tickets-table"] tbody tr').should('have.length.greaterThan', 0)
    cy.get('[data-testid="tickets-table"] tbody tr').first().click()
    
    // 3. Assigner le ticket
    cy.get('[data-testid="assign-ticket"]').click()
    cy.get('[data-testid="assignee-select"]').select('1')
    cy.get('[data-testid="confirm-assign"]').click()
    cy.get('.toast-success').should('be.visible')
    
    // 4. Ajouter une réponse
    cy.get('[data-testid="add-response"]').click()
    cy.get('[data-testid="response-content"]').type('This is a response to the ticket')
    cy.get('[data-testid="submit-response"]').click()
    cy.get('.toast-success').should('be.visible')
    
    // 5. Fermer le ticket
    cy.get('[data-testid="close-ticket"]').click()
    cy.get('[data-testid="confirm-close"]').click()
    cy.get('.toast-success').should('be.visible')
    
    // 6. Vérifier que le ticket est fermé
    cy.get('[data-testid="ticket-status"]').should('contain', 'Fermé')
  })

  it('should handle SMS webhook integration', () => {
    // Simuler un webhook SMS
    cy.request({
      method: 'POST',
      url: '/api/v1/channels/webhooks/sms/',
      body: {
        MessageSid: 'SM1234567890',
        MessageStatus: 'delivered',
        From: '+1234567890',
        To: '+0987654321',
        Body: 'Test SMS message'
      }
    }).then((response) => {
      expect(response.status).to.equal(200)
    })
    
    // Vérifier que le message est créé
    cy.visit('/channels')
    cy.get('[data-testid="messages-table"]').should('be.visible')
    cy.get('[data-testid="messages-table"] tbody tr').should('have.length.greaterThan', 0)
  })

  it('should handle WhatsApp webhook integration', () => {
    // Simuler un webhook WhatsApp
    cy.request({
      method: 'POST',
      url: '/api/v1/channels/webhooks/whatsapp/',
      body: {
        entry: [{
          changes: [{
            value: {
              messages: [{
                from: '1234567890',
                text: { body: 'Test WhatsApp message' }
              }]
            }
          }]
        }]
      }
    }).then((response) => {
      expect(response.status).to.equal(200)
    })
  })

  it('should handle email integration', () => {
    // Créer un ticket via email
    cy.visit('/tickets')
    cy.get('[data-testid="create-ticket-button"]').click()
    
    cy.get('input[name="title"]').type('Email Integration Test')
    cy.get('textarea[name="content"]').type('This ticket was created via email')
    cy.get('select[name="category"]').select('1')
    cy.get('select[name="priority"]').select('3')
    cy.get('select[name="channel"]').select('3') // Email channel
    
    cy.get('[data-testid="submit-ticket"]').click()
    cy.get('.toast-success').should('be.visible')
    
    // Vérifier que le ticket est créé
    cy.get('[data-testid="tickets-table"] tbody tr').should('have.length.greaterThan', 0)
  })

  it('should handle analytics integration', () => {
    // Créer plusieurs tickets pour les tests
    for (let i = 0; i < 5; i++) {
      cy.visit('/tickets')
      cy.get('[data-testid="create-ticket-button"]').click()
      
      cy.get('input[name="title"]').type(`Analytics Test Ticket ${i}`)
      cy.get('textarea[name="content"]').type(`Test content ${i}`)
      cy.get('select[name="category"]').select('1')
      cy.get('select[name="priority"]').select('3')
      cy.get('select[name="channel"]').select('4')
      
      cy.get('[data-testid="submit-ticket"]').click()
      cy.get('.toast-success').should('be.visible')
    }
    
    // Vérifier les analytics
    cy.visit('/analytics')
    cy.get('[data-testid="analytics"]').should('be.visible')
    cy.get('[data-testid="tickets-chart"]').should('be.visible')
    cy.get('[data-testid="categories-chart"]').should('be.visible')
  })

  it('should handle user management integration', () => {
    // Créer un nouvel utilisateur
    cy.visit('/users')
    cy.get('[data-testid="create-user-button"]').click()
    
    cy.get('input[name="username"]').type('integrationuser')
    cy.get('input[name="email"]').type('integration@example.com')
    cy.get('input[name="password"]').type('password123')
    cy.get('input[name="first_name"]').type('Integration')
    cy.get('input[name="last_name"]').type('User')
    
    cy.get('[data-testid="submit-user"]').click()
    cy.get('.toast-success').should('be.visible')
    
    // Vérifier que l'utilisateur est créé
    cy.get('[data-testid="users-table"] tbody tr').should('have.length.greaterThan', 0)
  })

  it('should handle channel management integration', () => {
    // Tester la gestion des canaux
    cy.visit('/channels')
    cy.get('[data-testid="channels-table"]').should('be.visible')
    
    // Tester un canal
    cy.get('[data-testid="channels-table"] tbody tr').first().click()
    cy.get('[data-testid="test-connection"]').click()
    cy.get('.toast-success').should('be.visible')
  })

  it('should handle error recovery integration', () => {
    // Simuler une erreur
    cy.intercept('GET', '/api/v1/tickets/tickets/', { statusCode: 500 })
    
    cy.visit('/tickets')
    
    // Vérifier que l'erreur est gérée
    cy.get('[data-testid="error-message"]').should('be.visible')
    cy.get('[data-testid="retry-button"]').click()
    
    // Vérifier que la récupération fonctionne
    cy.intercept('GET', '/api/v1/tickets/tickets/', { statusCode: 200, body: { results: [] } })
    cy.get('[data-testid="tickets-table"]').should('be.visible')
  })

  it('should handle data consistency integration', () => {
    // Créer un ticket
    cy.visit('/tickets')
    cy.get('[data-testid="create-ticket-button"]').click()
    
    cy.get('input[name="title"]').type('Consistency Test')
    cy.get('textarea[name="content"]').type('Test content')
    cy.get('select[name="category"]').select('1')
    cy.get('select[name="priority"]').select('3')
    cy.get('select[name="channel"]').select('4')
    
    cy.get('[data-testid="submit-ticket"]').click()
    cy.get('.toast-success').should('be.visible')
    
    // Modifier le ticket
    cy.get('[data-testid="tickets-table"] tbody tr').first().click()
    cy.get('[data-testid="edit-ticket"]').click()
    
    cy.get('input[name="title"]').clear().type('Updated Title')
    cy.get('[data-testid="save-ticket"]').click()
    cy.get('.toast-success').should('be.visible')
    
    // Vérifier que les modifications sont persistées
    cy.get('[data-testid="ticket-title"]').should('contain', 'Updated Title')
  })

  it('should handle performance integration', () => {
    // Mesurer les performances
    const startTime = Date.now()
    
    cy.visit('/dashboard')
    cy.get('[data-testid="dashboard"]').should('be.visible')
    
    const loadTime = Date.now() - startTime
    expect(loadTime).to.be.lessThan(3000)
    
    // Vérifier que les composants se chargent rapidement
    cy.get('[data-testid="dashboard-stats"]').should('be.visible')
    cy.get('[data-testid="recent-tickets"]').should('be.visible')
    cy.get('[data-testid="quick-actions"]').should('be.visible')
  })

  it('should handle security integration', () => {
    // Tester l'authentification
    cy.visit('/dashboard')
    cy.get('[data-testid="dashboard"]').should('be.visible')
    
    // Tester la déconnexion
    cy.get('[data-testid="user-menu"]').click()
    cy.get('[data-testid="logout-button"]').click()
    
    cy.url().should('include', '/login')
    
    // Tester la reconnexion
    cy.get('input[name="username"]').type('admin')
    cy.get('input[name="password"]').type('admin123')
    cy.get('button[type="submit"]').click()
    
    cy.url().should('include', '/dashboard')
  })

  it('should handle mobile integration', () => {
    // Tester sur mobile
    cy.viewport(375, 667)
    cy.visit('/dashboard')
    
    cy.get('[data-testid="mobile-menu"]').should('be.visible')
    cy.get('[data-testid="dashboard"]').should('be.visible')
    
    // Tester la navigation mobile
    cy.get('[data-testid="mobile-menu-button"]').click()
    cy.get('[data-testid="mobile-menu"]').should('be.visible')
    
    cy.get('[data-testid="tickets-link"]').click()
    cy.url().should('include', '/tickets')
  })

  it('should handle accessibility integration', () => {
    // Tester l'accessibilité
    cy.visit('/dashboard')
    
    // Vérifier la navigation au clavier
    cy.get('body').tab()
    cy.focused().should('be.visible')
    
    // Vérifier les attributs ARIA
    cy.get('[data-testid="dashboard"]').should('have.attr', 'role')
    cy.get('[data-testid="tickets-table"]').should('have.attr', 'role', 'table')
  })

  it('should handle internationalization integration', () => {
    // Tester la localisation
    cy.visit('/dashboard')
    
    // Vérifier que l'interface est en français
    cy.get('html').should('have.attr', 'lang', 'fr')
    
    // Vérifier que les textes sont localisés
    cy.get('[data-testid="dashboard-title"]').should('contain', 'Tableau de bord')
  })
})