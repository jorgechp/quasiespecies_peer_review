import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'app-partition-representation',
  templateUrl: './partition-representation.component.html'
})
export class PartitionRepresentationComponent implements OnInit {

  @Input() partitionId: number;

  constructor() {
    this.partitionId = 0;
  }

  ngOnInit(): void { }

}
