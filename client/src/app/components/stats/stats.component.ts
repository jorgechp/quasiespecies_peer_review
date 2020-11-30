import { TrainService } from '@src/app/services/train.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { UserScoreRow, UserScoreTable } from '@src/app/models/user-score-table.model';
import { SubmissionProfileInterface } from '@src/app/models/submission-profile-interface';
import { TypeOfJournal } from '@src/app/models/type-of-journal.enum';
import { PartitionInterface } from '@src/app/models/partition-interface';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit, OnDestroy {

  private trainServiceSuscription: Subscription | undefined;
  public confusionMatrixDataFull: UserScoreTable | undefined;
  public partition: PartitionInterface | undefined;
  public submissionProfile: SubmissionProfileInterface | undefined;

  numberOfAnswers = 0;

  totalHigh = 0;
  totalLow = 0;
  totalMedium = 0;

  limit = 0.6;

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

  generatePartitionString(): string{
    const partitionAsArray = Array<Array<TypeOfJournal>>();

    if (this.partition !== undefined){
      if (this.partition.LOW){
        partitionAsArray.push([TypeOfJournal.LOW]);
      }

      if (this.partition.MEDIUM){
        partitionAsArray.push([TypeOfJournal.MEDIUM]);
      }

      if (this.partition.HIGH){
        partitionAsArray.push([TypeOfJournal.HIGH]);
      }
    }
    return '';
  }

  private infereProfileSubmission(profileData: UserScoreRow): Array<TypeOfJournal>{
    const profile = Array<TypeOfJournal>();
    if (profileData?.LOW >= this.limit){
      profile.push(TypeOfJournal.LOW);
    }
    if (profileData?.MEDIUM >= this.limit){
      profile.push(TypeOfJournal.MEDIUM);
    }
    if ( profileData?.HIGH >= this.limit){
      profile.push(TypeOfJournal.HIGH);
    }
    return profile;
  }

  private inferePartition(): PartitionInterface | undefined{
    if (this.confusionMatrixDataFull !== undefined){
      const partition = {LOW: false, MEDIUM: false,
                         HIGH: false, LOW_HIGH: false,
                         LOW_MEDIUM: false,
                         MEDIUM_HIGH: false} as PartitionInterface;

      if (this.confusionMatrixDataFull.LOW.LOW >= this.limit){
        partition.LOW = true;
      }

      if (this.confusionMatrixDataFull.LOW.MEDIUM >= this.limit && this.confusionMatrixDataFull.MEDIUM.LOW >= this.limit){
        partition.LOW_MEDIUM = true;
      }

      if (this.confusionMatrixDataFull.LOW.HIGH >= this.limit && this.confusionMatrixDataFull.HIGH.LOW >= this.limit){
        partition.LOW_HIGH = true;
      }

      if (this.confusionMatrixDataFull.MEDIUM.MEDIUM >= this.limit){
        partition.MEDIUM = true;
      }

      if (this.confusionMatrixDataFull.MEDIUM.HIGH >= this.limit && this.confusionMatrixDataFull.HIGH.MEDIUM >= this.limit){
        partition.MEDIUM_HIGH = true;
      }

      if (this.confusionMatrixDataFull.HIGH.HIGH >= this.limit){
        partition.HIGH = true;
      }
      return partition;
    }
    return undefined;
  }

  private infereSubmissionProfile(): SubmissionProfileInterface | undefined{
    if (this.confusionMatrixDataFull !== undefined){
      const lowProfile = this.infereProfileSubmission(this.confusionMatrixDataFull.LOW);
      const mediumProfile = this.infereProfileSubmission(this.confusionMatrixDataFull.MEDIUM);
      const highProfile = this.infereProfileSubmission(this.confusionMatrixDataFull.HIGH);
      return {LOW: lowProfile, MEDIUM: mediumProfile, HIGH: highProfile} as SubmissionProfileInterface;
    }
    return undefined;
  }

  subscribeTrainService(): void {
    this.trainServiceSuscription = this.trainService.getScoreTable().subscribe(
      (response: UserScoreTable) => {
        this.confusionMatrixDataFull = response;
        this.computeBasicStats();
        this.partition = this.inferePartition();
        this.submissionProfile = this.infereSubmissionProfile();
      }
    );
  }



}
