import { Component, inject, signal } from '@angular/core';
import { IMaintenance } from '../../interfaces/maintenance.interface';
import { MaintenanceService } from '../../service/maintenance';
import { FormsModule, NgForm } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-maintenance',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './maintenance.html',
  styleUrls: ['./maintenance.scss']
})
export class Maintenance {
  private maintenanceService = inject(MaintenanceService);

  maintenances = this.maintenanceService.maintenances;

  today = new Date().toISOString().split('T')[0]; // pour min="today"

  newMaintenance = signal<IMaintenance>({
    Description: '',
    PropertyID: 0,
    ScheduledDate: '',
    Status: '',
    TaskID: 0
  });

  editMode = signal(false);
  selectedId = signal<number | null>(null);

  ngOnInit() {
    this.maintenanceService.getMaintenances().subscribe();
  }

  addMaintenance(form: NgForm) {
    if (form.invalid) {
      alert('⚠️ Veuillez remplir tous les champs');
      return;
    }

    const maintenance = { ...this.newMaintenance() };
    this.maintenanceService.createMaintenances(maintenance).subscribe({
      next: created => {
        this.maintenances.update(list => [...list, created]);
        this.resetForm();
        form.resetForm();
      },
      error: err => console.error('❌ Erreur création :', err)
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

    const maintenance = { ...this.newMaintenance() };
    this.maintenanceService.patchMaintenances(id, maintenance).subscribe({
      next: updated => {
        this.maintenances.update(list =>
          list.map(p => (p.TaskID === id ? updated : p))
        );
        this.resetForm();
        form.resetForm();
      },
      error: err => console.error('❌ Erreur update :', err)
    });
  }

  confirmDelete(id: number) {
    if (confirm('⚠️ Are you sure you want to delete this maintenance?')) {
      this.deleteMaintenance(id);
    }
  }

  deleteMaintenance(id: number) {
    this.maintenanceService.deleteMaintenance(id).subscribe({
      next: () => {
        this.maintenances.update(list => list.filter(p => p.TaskID !== id));
      },
      error: err => console.error('❌ Erreur delete :', err)
    });
  }

  sortByDate() {
    this.maintenances.update(list =>
      [...list].sort((a, b) => new Date(a.ScheduledDate).getTime() - new Date(b.ScheduledDate).getTime())
    );
  }

  cancelEdit() {
    this.resetForm();
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

  trackById(index: number, item: IMaintenance) {
    return item.TaskID;
  }
}
