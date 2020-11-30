import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConfussionMatrixComponent } from '@src/app/app/stats/confussion-matrix/confussion-matrix.component';

describe('ConfussionMatrixComponent', () => {
  let component: ConfussionMatrixComponent;
  let fixture: ComponentFixture<ConfussionMatrixComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ConfussionMatrixComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ConfussionMatrixComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
