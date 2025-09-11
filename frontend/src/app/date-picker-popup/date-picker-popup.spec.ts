import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DatePickerPopup } from './date-picker-popup';

describe('DatePickerPopup', () => {
  let component: DatePickerPopup;
  let fixture: ComponentFixture<DatePickerPopup>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DatePickerPopup]
    })
    .compileComponents();

    fixture = TestBed.createComponent(DatePickerPopup);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
