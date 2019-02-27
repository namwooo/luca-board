import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ContentOnlyLayoutComponent } from './content-only-layout.component';

describe('ContentOnlyLayoutComponent', () => {
  let component: ContentOnlyLayoutComponent;
  let fixture: ComponentFixture<ContentOnlyLayoutComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ContentOnlyLayoutComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ContentOnlyLayoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
