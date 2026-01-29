// ============================================================================
// API Path Constants
// ============================================================================
// This file contains sales API endpoint paths for the application.
// Updated: Jan 30, 2026 - Sales APIs only
// ============================================================================

export const API_PATH = {
  SALES: {
    CAMPAIGNS: {
      CREATE: "/api/sales/campaigns",
      LIST: "/api/sales/campaigns",
      GET_BY_ID: (campaign_id: string) => `/api/sales/campaigns/${campaign_id}`,
      UPDATE: (campaign_id: string) => `/api/sales/campaigns/${campaign_id}`,
      DELETE: (campaign_id: string) => `/api/sales/campaigns/${campaign_id}`,
      LIST_ACTIVE: "/api/sales/campaigns/active",
    },
    LEADS: {
      CREATE: "/api/sales/leads",
      LIST: "/api/sales/leads",
      GET_BY_ID: (lead_id: string) => `/api/sales/leads/${lead_id}`,
      UPDATE: (lead_id: string) => `/api/sales/leads/${lead_id}`,
      DELETE: (lead_id: string) => `/api/sales/leads/${lead_id}`,
      LIST_BY_CAMPAIGN: (campaign_id: string) => `/api/sales/leads/campaign/${campaign_id}`,
      LIST_BY_STATUS: (status_id: string) => `/api/sales/leads/status/${status_id}`,
    },
    PROPOSALS: {
      CREATE: "/api/sales/proposals",
      LIST: "/api/sales/proposals",
      GET_BY_ID: (proposal_id: string) => `/api/sales/proposals/${proposal_id}`,
      UPDATE: (proposal_id: string) => `/api/sales/proposals/${proposal_id}`,
      DELETE: (proposal_id: string) => `/api/sales/proposals/${proposal_id}`,
      LIST_BY_STATUS: (status_id: string) => `/api/sales/proposals/status/${status_id}`,
      LIST_BY_COMPANY: (company_id: string) => `/api/sales/proposals/company/${company_id}`,
      RECIPIENTS: {
        ADD: (proposal_id: string) => `/api/sales/proposals/${proposal_id}/recipients`,
        LIST: (proposal_id: string) => `/api/sales/proposals/${proposal_id}/recipients`,
        GET_BY_ID: (proposal_id: string, recipient_id: string) => `/api/sales/proposals/${proposal_id}/recipients/${recipient_id}`,
        UPDATE: (proposal_id: string, recipient_id: string) => `/api/sales/proposals/${proposal_id}/recipients/${recipient_id}`,
        DELETE: (proposal_id: string, recipient_id: string) => `/api/sales/proposals/${proposal_id}/recipients/${recipient_id}`,
      },
      SUBMISSIONS: {
        CREATE: (proposal_id: string) => `/api/sales/proposals/${proposal_id}/submissions`,
        LIST: (proposal_id: string) => `/api/sales/proposals/${proposal_id}/submissions`,
        GET_BY_ID: (proposal_id: string, submission_id: string) => `/api/sales/proposals/${proposal_id}/submissions/${submission_id}`,
        UPDATE: (proposal_id: string, submission_id: string) => `/api/sales/proposals/${proposal_id}/submissions/${submission_id}`,
      },
    },
  },
};
