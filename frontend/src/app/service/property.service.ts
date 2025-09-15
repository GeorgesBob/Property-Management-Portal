import { Injectable, inject, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { IProperty } from '../interfaces/property.interface';
import { catchError } from 'rxjs/operators';
import { environment } from '../../environnement/environnement'; 
@Injectable({
  providedIn: 'root'
})

export class PropertyService {
  private http = inject(HttpClient);
  readonly properties = signal<IProperty[]>([]);
  readonly url = `${environment.apiUrl}property`;

  getProperties (): Observable<IProperty[]> {
    return this.http.get<IProperty[]>(this.url).pipe(tap(properties => this.properties.set(properties)));
  }

  createProperties(property: Omit<IProperty, 'PropertyID'>): Observable<IProperty> {
    return this.http.post<IProperty>(`${this.url}/`, property);
  }

  patchProperties(id: number, changes: Partial<IProperty>): Observable<IProperty> {
    console.log("Id number :", id);

    return this.http.patch<IProperty>(`${this.url}/${id}`, changes).pipe(catchError(error => {
      throw error;
    })
  );
  }

  deleteProperty(id: number): Observable<void> {
    return this.http.delete<void>(`${this.url}/${id}`);
  }


}
