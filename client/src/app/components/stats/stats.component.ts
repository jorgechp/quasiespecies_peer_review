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

  public confusionMatrixData: UserScoreTable | undefined;
  public displayedColumns: string[] = ['intro', 'target', 'LOW', 'MEDIUM', 'HIGH'];

  constructor(private trainService: TrainService) {
    this.confusionMatrixData = undefined;
  }

  ngOnInit(): void {
    this.subscribeTrainService();
  }

  ngOnDestroy(): void{
    if (this.trainServiceSuscription !== undefined){
      this. trainServiceSuscription?.unsubscribe();
    }
  }

  subscribeTrainService(): void {
    this.trainServiceSuscription = this.trainService.getScoreTable().subscribe(
      (response: UserScoreTable) => {
        this.confusionMatrixData = response;
        console.log(response.HIGH.HIGH);
      }
    );
  }



}
