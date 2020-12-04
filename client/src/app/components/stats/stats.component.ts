import { TrainService } from '@src/app/services/train.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { UserScore, UserScorePartition, UserScoreTable } from '@src/app/models/user-score.model';
import { SubmissionProfileInterface } from '@src/app/models/submission-profile-interface';
import { UserService } from '@src/app/services/user.service';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit, OnDestroy {

  private trainServiceSuscription: Subscription | undefined;
  private partitionsKey: [] | undefined;
  private partitions: (number)[][] | undefined;

  public confusionMatrixDataFull: UserScoreTable | undefined;
  public partition: UserScorePartition | undefined;
  public submissionProfile: SubmissionProfileInterface | undefined;
  loginSuscription: Subscription | undefined;

  numberOfAnswers = 0;

  totalHigh = 0;
  totalLow = 0;
  totalMedium = 0;

  limit = 0.6;

  isLogged = false;
  submissionProfile: object;

  constructor(private trainService: TrainService,
              private userService: UserService) {
    this.confusionMatrixDataFull = undefined;
  }

  ngOnInit(): void {
    this.subscribeCheckLogin();
    this.subscribeTrainService();
  }

  ngOnDestroy(): void{
    if (this.trainServiceSuscription !== undefined){
      this. trainServiceSuscription?.unsubscribe();
    }
    if (this.loginSuscription !== undefined){
      this.loginSuscription.unsubscribe();
    }
  }

  subscribeCheckLogin(): void{
    this.loginSuscription = this.userService.checkLogin().subscribe(
      (isLogged: boolean) => {
        this.isLogged = isLogged;
      }
    );
  }

  private computeBasicStats(): void{
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
      (response: UserScore) => {
        this.confusionMatrixDataFull = response.score_table;
        this.computeBasicStats();
        this.partitionsKey = response.user_partitions.partitions_keys;
        const partitions = response.user_partitions.partitions;
        const keys = Object.keys(partitions);
        const sortedKeys = keys.sort((key1, key2) => partitions[Number(key2)] - partitions[Number(key1)]);
        const partitionsSorted = sortedKeys.map((key) => [Number(key), partitions[Number(key)]]);
        this.partition = ({id_partition: partitionsSorted[0][0], score_partition: partitionsSorted[0][1]} as UserScorePartition);
        this.submissionProfile = response.user_partitions.submissions[this.partition.id_partition];
        console.log(this.submissionProfile);
      }
    );
  }



}
