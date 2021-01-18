import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PartitionRepresentationComponent } from '@src/app/components/stats/partition-representation/partition-representation.component';

describe('PartitionRepresentationComponent', () => {
  let component: PartitionRepresentationComponent;
  let fixture: ComponentFixture<PartitionRepresentationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PartitionRepresentationComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PartitionRepresentationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
