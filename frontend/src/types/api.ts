export interface ApiResponse<T> {
  data: T;
  message: string;
  statusCode: number;
}

export interface ErrorResponse {
  detail: string;
  code?: string;
}
