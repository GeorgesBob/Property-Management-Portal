import { HttpClient } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { IMaintenance } from '../interfaces/maintenance.interface';
import { Observable, catchError, tap } from 'rxjs';
import { environment } from '../../environnement/environnement';

@Injectable({
  providedIn: 'root'
})
export class MaintenanceService {
  private http = inject(HttpClient);
  readonly maintenances = signal<IMaintenance[]>([]);
  readonly url = `${environment.apiUrl}maintenance`;

  getMaintenances (): Observable<IMaintenance[]> {
    return this.http.get<IMaintenance[]>(this.url).pipe(tap(maintenances => this.maintenances.set(maintenances)));
  }

  createMaintenances(maintenance: Omit<IMaintenance, 'TaskID'>): Observable<IMaintenance> {
    return this.http.post<IMaintenance>(`${this.url}/`, maintenance);
  }

  patchMaintenances(id: number, changes: Partial<IMaintenance>): Observable<IMaintenance> {
    console.log("Id number :", id);

    return this.http.patch<IMaintenance>(`${this.url}/${id}`, changes).pipe(catchError(error => {
      throw error;
    })
  );
  }

  deleteMaintenance(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/${id}`);
  }
}
