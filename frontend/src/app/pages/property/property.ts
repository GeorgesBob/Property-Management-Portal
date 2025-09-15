import { Component, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, NgForm } from '@angular/forms';
import { PropertyService } from '../../service/property.service';
import { IProperty } from '../../interfaces/property.interface';

@Component({
  selector: 'app-property',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './property.html',
  styleUrls: ['./property.scss']
})
export class PropertyComponent {
  private propertyService = inject(PropertyService);

  properties = this.propertyService.properties;

  today = new Date().toISOString().split('T')[0];

  // State
  newProperty = signal<IProperty>({
    Address: '',
    Price: 0,
    PropertyID: 0,
    PurchaseDate: '',
    Status: '',
    PropertyType: ''
  });

  editMode = signal(false);
  selectedId = signal<number | null>(null);

  ngOnInit() {
    this.propertyService.getProperties().subscribe();
  }

  addProperty(form: NgForm) {
    if (form.invalid) {
      alert('⚠️ Veuillez remplir tous les champs');
      return;
    }

    const property = { ...this.newProperty() };
    this.propertyService.createProperties(property).subscribe({
      next: created => {
        this.properties.update(list => [...list, created]);
        this.resetForm();
        form.resetForm();
      },
      error: err => console.error('❌ Erreur création :', err)
    });
  }

  editProperty(property: IProperty) {
    this.editMode.set(true);
    this.selectedId.set(property.PropertyID);
    this.newProperty.set({ ...property });
  }

  cancelEdit() {
    this.resetForm();
  }

  updateProperty(form: NgForm) {
    if (form.invalid) {
      alert('⚠️ Veuillez remplir tous les champs');
      return;
    }

    const id = this.selectedId();
    if (!id) return;

    const property = { ...this.newProperty() };
    this.propertyService.patchProperties(id, property).subscribe({
      next: updated => {
        this.properties.update(list =>
          list.map(p => (p.PropertyID === id ? updated : p))
        );
        this.resetForm();
        form.resetForm();
      },
      error: err => console.error('❌ Erreur update :', err)
    });
  }

  confirmDelete(id: number) {
    if (confirm('⚠️ Are you sure you want to delete this property?')) {
      this.deleteProperty(id);
    }
  }

  deleteProperty(id: number) {
    this.propertyService.deleteProperty(id).subscribe({
      next: () => {
        this.properties.update(list => list.filter(p => p.PropertyID !== id));
      },
      error: err => console.error('❌ Erreur delete :', err)
    });
  }

  resetForm() {
    this.newProperty.set({
      Address: '',
      Price: 0,
      PropertyID: 0,
      PurchaseDate: '',
      Status: '',
      PropertyType: ''
    });
    this.editMode.set(false);
    this.selectedId.set(null);
  }

  trackById(index: number, item: IProperty) {
    return item.PropertyID;
  }
}
