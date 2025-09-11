import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { PropertyComponent } from './pages/property/property';
import {TenantComponent } from './pages/tenant/tenant';
import { Maintenance } from './pages/maintenance/maintenance';

export const routes: Routes = [
  { path: 'property', component: PropertyComponent },
  { path: 'tenant', component: TenantComponent },
  { path: 'maintenance', component: Maintenance },
  { path: '', redirectTo: 'property', pathMatch: 'full' }, // redirection par défaut
  { path: '**', redirectTo: 'property' } // fallback si route inconnue
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
