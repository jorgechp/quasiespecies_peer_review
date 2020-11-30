import { TrainService } from '@src/app/services/train.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { UserScoreTable } from '@src/app/models/user-score-table.model';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit, OnDestroy {

  private trainServiceSuscription: Subscription | undefined;
  public confusionMatrixDataFull: UserScoreTable | undefined;

  numberOfAnswers = 0;

  totalHigh = 0;
  totalLow = 0;
  totalMedium = 0;

  constructor(private trainService: TrainService) {
    this.confusionMatrixDataFull = undefined;
  }

  ngOnInit(): void {
    this.subscribeTrainService();
  }

  ngOnDestroy(): void{
    if (this.trainServiceSuscription !== undefined){
      this. trainServiceSuscription?.unsubscribe();
    }
  }

  computeStats(): void{
    if (this.confusionMatrixDataFull !== undefined){
      let sum = 0;
      let minimumValue = Number.MAX_SAFE_INTEGER;
      let maximumValue = Number.MIN_SAFE_INTEGER;
      let maximumCoordinate: Array<string>;
      let minimumCoordinate: Array<string>;

      let totalRow = 0;
      for (const [key, value] of Object.entries(this.confusionMatrixDataFull)) {
        for (const [subKey, subValue] of Object.entries(value)){
          const score = subValue as number;
          totalRow += score;
          console.log(subKey, subValue);
          if (minimumValue > score){
            minimumValue = score;
            minimumCoordinate = [key, subKey];
          }else if (maximumValue < score){
            maximumValue = score;
            maximumCoordinate = [key, subKey];
          }
        }
        sum += totalRow;
        switch (key){
          case 'HIGH':
            this.totalHigh = totalRow;
            break;
          case 'MEDIUM':
              this.totalMedium = totalRow;
              break;
          case 'LOW':
              this.totalLow = totalRow;
              break;
        }
        totalRow = 0;
      }

      this.numberOfAnswers = sum;
    }
  }

  subscribeTrainService(): void {
    this.trainServiceSuscription = this.trainService.getScoreTable().subscribe(
      (response: UserScoreTable) => {
        this.confusionMatrixDataFull = response;
        this.computeStats();
      }
    );
  }



}
