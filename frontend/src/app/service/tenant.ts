import { HttpClient } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { Observable, catchError, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TenantService {
  private http = inject(HttpClient);
  readonly tenants = signal<ITenant[]>([]);
  readonly url = 'http://127.0.0.1:8000/tenant';

  getTenants (): Observable<ITenant[]> {
    return this.http.get<ITenant[]>(this.url).pipe(tap(tenants => this.tenants.set(tenants)));
  }

  createTenants(tenant: Omit<ITenant, 'TenantID'>): Observable<ITenant> {
    return this.http.post<ITenant>(`${this.url}/`, tenant);
  }

  patchTenants(id: number, changes: Partial<ITenant>): Observable<ITenant> {
    console.log("Id number :", id);

    return this.http.patch<ITenant>(`${this.url}/${id}`, changes).pipe(catchError(error => {
      throw error;
    })
  );
  }

  deleteTenant(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/${id}`);
  }
}
