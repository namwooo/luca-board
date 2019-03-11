import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PostRankComponent } from './post-rank.component';

describe('PostRankComponent', () => {
  let component: PostRankComponent;
  let fixture: ComponentFixture<PostRankComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ PostRankComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PostRankComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
