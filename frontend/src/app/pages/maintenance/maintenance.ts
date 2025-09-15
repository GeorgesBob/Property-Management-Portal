import { Component, inject, signal } from '@angular/core';
import { IMaintenance } from '../../interfaces/maintenance.interface';
import { MaintenanceService } from '../../service/maintenance';
import { FormsModule, NgForm } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { PropertyService } from '../../service/property.service';

@Component({
  selector: 'app-maintenance',
  imports: [CommonModule, FormsModule],
  templateUrl: './maintenance.html',
  styleUrl: './maintenance.scss'
})
export class Maintenance {
  private maintenanceService = inject(MaintenanceService);
  maintenances = this.maintenanceService.maintenances;

  today = new Date().toISOString().split('T')[0]; // pour min="today"

  // State
  newMaintenance = signal<IMaintenance>({
    Description: '',
    PropertyID: 0,
    ScheduledDate: '',
    Status: '',
    TaskID: 0
  });

  editMode = signal(false);
  selectedId = signal<number | null>(null);
  propertyId = signal<number | null>(null);

  ngOnInit() {
    this.maintenanceService.getMaintenances().subscribe();
  }

  addMaintenance(form: NgForm) {
    if (form.invalid) {
      alert('⚠️ Veuillez remplir tous les champs');
      return;
    }

    const maintenance = this.newMaintenance();
    const maintenances = {
      Description: maintenance.Description,
      PropertyID: maintenance.PropertyID,
      ScheduledDate: maintenance.ScheduledDate,
      Status: maintenance.Status
    }



    this.maintenanceService.createMaintenances(maintenances).subscribe({
      next: created => {
        created = maintenance
        this.maintenances.update(list => [...list, created]);
        this.resetForm();
        form.resetForm();
      },
      error: err => console.error('Erreur création :', err)
    });
  }

  editMaintenance(maintenance: IMaintenance) {
    this.editMode.set(true);
    this.selectedId.set(maintenance.TaskID);
    this.newMaintenance.set({ ...maintenance });
  }

  updateMaintenance(form: NgForm) {
    if (form.invalid) {
      alert('⚠️ Veuillez remplir tous les champs');
      return;
    }

    const id = this.selectedId();
    if (!id) return;

    this.maintenanceService.patchMaintenances(id, this.newMaintenance()).subscribe({
      next: updated => {
        updated = this.newMaintenance()
        this.maintenances.update(list =>
          list.map(p => (p.TaskID === id ? updated : p))
        );
        this.resetForm();
        form.resetForm();
      },
      error: err => console.error('❌ Erreur update :', err)
    });
  }

  deleteMaintenance(id: number) {
    this.maintenanceService.deleteMaintenance(id).subscribe({
      next: () => {
        this.maintenances.update(list => list.filter(p => p.TaskID !== id));
      },
      error: err => console.error('❌ Erreur delete :', err)
    });
  }

  resetForm() {
    this.newMaintenance.set({
      Description: '',
      PropertyID: 0,
      ScheduledDate: '',
      Status: '',
      TaskID: 0
    });
    this.editMode.set(false);
    this.selectedId.set(null);
  }
}
