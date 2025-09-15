import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import { TenantService } from '../../service/tenant.js';


@Component({
  selector: 'app-Tenant',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './Tenant.html',
  styleUrls: ['./Tenant.scss']
})
export class TenantComponent {
  private tenantService = inject(TenantService);

  tenants = this.tenantService.tenants;

  today = new Date().toISOString().split('T')[0]; // pour min="today"

  // State
  newTenant = signal<ITenant>({
    TenantID: 0,
    Name: '',
    ContactInfo: '',
    LeaseTermStart: '',
    LeaseTermEnd: '',
    RentalPaymentStatus: '',
    PropertyID: 0
  });


  editMode = signal(false);
  selectedId = signal<number | null>(null);

  ngOnInit() {
    this.tenantService.getTenants().subscribe();
  }

  addTenant(form: NgForm) {
    if (form.invalid) {
      alert('Veuillez remplir tous les champs');
      return;
    }

    const tenant = this.newTenant();
    
    let leaseTermStart = new Date(tenant.LeaseTermStart);
    let leaseTermEnd = new Date(tenant.LeaseTermEnd)

    if (leaseTermStart < leaseTermEnd){
    const tent = {
    Name: tenant.Name,
    ContactInfo: tenant.ContactInfo,
    LeaseTermStart: tenant.LeaseTermStart,
    LeaseTermEnd: tenant.LeaseTermEnd,
    RentalPaymentStatus: tenant.RentalPaymentStatus,
    PropertyID: tenant.PropertyID
    }
    
    this.tenantService.createTenants(tent).subscribe({
      next: created => {
        created = tenant
        this.tenants.update(list => [...list, created]);
        this.resetForm();
        form.resetForm();
      },
      error: err => console.error('Erreur création :', err)
    });
    } else {
      alert('LeaseTermStart date is bigger than LeaseTermEnd date');
    }
  }

  editTenant(Tenant: ITenant) {
    this.editMode.set(true);
    this.selectedId.set(Tenant.TenantID);
    this.newTenant.set({ ...Tenant });
  }

  updateTenant(form: NgForm) {
    if (form.invalid) {
      alert('Veuillez remplir tous les champs');
      return;
    }

    const id = this.selectedId();
    if (!id) return;

    this.tenantService.patchTenants(id, this.newTenant()).subscribe({
      next: updated => {
        updated = this.newTenant()
        this.tenants.update(list =>
          list.map(p => (p.TenantID === id ? updated : p))
        );
        this.resetForm();
        form.resetForm();
      },
      error: err => console.error('Erreur update :', err)
    });
  }

  deleteTenant(id: number) {
    this.tenantService.deleteTenant(id).subscribe({
      next: () => {
        this.tenants.update(list => list.filter(p => p.TenantID !== id));
      },
      error: err => console.error('Erreur delete :', err)
    });
  }

  resetForm() {
    this.newTenant.set({
      TenantID: 0,
      Name: '',
      ContactInfo: '',
      LeaseTermStart: '',
      LeaseTermEnd: '',
      RentalPaymentStatus: '',
      PropertyID: 0
    });
    this.editMode.set(false);
    this.selectedId.set(null);
  }
}

