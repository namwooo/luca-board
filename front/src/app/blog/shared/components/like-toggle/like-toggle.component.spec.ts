import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LikeToggleComponent } from './like-toggle.component';

describe('LikeToggleComponent', () => {
  let component: LikeToggleComponent;
  let fixture: ComponentFixture<LikeToggleComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LikeToggleComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LikeToggleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
