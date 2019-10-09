export interface TokenResponse {
  searchTerm: string;
  tokens: Token[];
}

export interface Token {
  token: string;
  tokenType: string;
}

export interface ClassificationResponse {
  searchTerm: string;
  classifications: Classification[];
}

export interface Classification {
  classificationType: string;
  matchingTokens: string[];
  nonMatchingTokens: string[];
  confidence: string;
}
