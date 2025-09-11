import { Component } from '@angular/core';
import { NgbAlertModule, NgbDatepickerModule, NgbDateStruct } from '@ng-bootstrap/ng-bootstrap';
import { FormsModule } from '@angular/forms';
@Component({
  selector: 'app-date-picker-popup',
  imports: [NgbDatepickerModule, NgbAlertModule, FormsModule, ],
  standalone: true, // ✅ must have this
	templateUrl: './date-picker-popup.html',
  styleUrl: './date-picker-popup.scss'
})
export class DatePickerPopup {
  model!: NgbDateStruct;
}
