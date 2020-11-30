import { Component, Input, OnInit } from '@angular/core';
import { UserScoreTable } from '@src/app/models/user-score-table.model';

@Component({
  selector: 'app-confusion-matrix',
  templateUrl: './confusion-matrix.component.html',
  styleUrls: ['./confusion-matrix.component.css']
})
export class ConfusionMatrixComponent implements OnInit {

  public displayedColumns: string[] = ['intro', 'target', 'LOW', 'MEDIUM', 'HIGH'];
  public isShownRelative = false;

  @Input() confusionMatrixData: UserScoreTable | undefined;
  @Input() highFactor = 1;
  @Input() mediumFactor = 1;
  @Input() lowFactor = 1;
  @Input() footer = '';
  @Input() maxLimit = 0;


  constructor() { }


  ngOnInit(): void {
    console.log('hola');
  }

}
