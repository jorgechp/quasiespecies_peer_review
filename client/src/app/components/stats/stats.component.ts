import { SubmissionProfileSubPartition } from '@src/app/models/submission-profile-interface';
import { UserScore, UserScoreRow } from '@src/app/models/user-score.model';
import { TrainService } from '@src/app/services/train.service';
import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { UserScorePartition, UserScoreTable } from '@src/app/models/user-score.model';
import { SubmissionProfileInterface } from '@src/app/models/submission-profile-interface';
import { UserService } from '@src/app/services/user.service';
import { TypeOfJournal } from '@src/app/models/type-of-journal.enum';

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent implements OnInit, OnDestroy {

  public TypeOfJournal = TypeOfJournal;
  private trainServiceSuscription: Subscription | undefined;
  private trainServiceEvolutionSuscription: Subscription | undefined;
  private loginSuscription: Subscription | undefined;

  private partitionsKey: [] | undefined;
  private partitions: (number)[][] | undefined;

  public confusionMatrixDataFull: UserScoreTable | undefined;
  public partition: UserScorePartition | undefined;
  public submissionProfile: SubmissionProfileInterface | undefined;
  public evolutionItems: { index: number; id_partition: number; id_submission_profile: string; }[] | undefined;
  public columnsToDisplay = ['index', 'id_partition', 'id_submission_profile'];


  numberOfAnswers = 0;

  totalHigh = 0;
  totalLow = 0;
  totalMedium = 0;

  limit = 0.5;

  isLogged = false;

  // submissionProfile: object;

  constructor(private trainService: TrainService,
              private userService: UserService) {
    this.confusionMatrixDataFull = undefined;
  }

  ngOnInit(): void {
    this.subscribeCheckLogin();
    this.subscribeTrainServiceEvolution();
  }

  ngOnDestroy(): void{
    if (this.trainServiceSuscription !== undefined){
      this. trainServiceSuscription?.unsubscribe();
    }
    if (this.trainServiceEvolutionSuscription !== undefined){
      this.trainServiceEvolutionSuscription.unsubscribe();
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

  private processPartition(response: UserScore): number[][] {
    const partitions = response.user_partitions.partitions;
    const keys = Object.keys(partitions);
    const sortedKeys = keys.sort((key1, key2) => partitions[Number(key2)] - partitions[Number(key1)]);
    const partitionsSorted = sortedKeys.map((key) => [Number(key), partitions[Number(key)]]);
    return partitionsSorted;
  }

  private processSubmissionProfile(submissionProfileResponse: Array<UserScoreRow>): Array<SubmissionProfileSubPartition>{
    const submissionProfile: SubmissionProfileSubPartition[] = [];
    submissionProfileResponse.forEach((score: UserScoreRow) => {
      const scoreRowAsList = [
        {impact: TypeOfJournal.HIGH, score: score.HIGH},
        {impact: TypeOfJournal.MEDIUM, score: score.MEDIUM},
        {impact: TypeOfJournal.LOW, score: score.LOW},
      ];

      const max = scoreRowAsList.reduce((prev, current) => {
        return (prev.score > current.score) ? prev : current;
      });

      submissionProfile.push(max);
    });
    return submissionProfile;
  }

  private processEvolution(userScoreTables: Array<UserScore>): void{
    const itemsTable: { index: number; id_partition: number; id_submission_profile: string; }[] = [];
    let step = 1;
    let lastLowImpact = '';
    let lastPartition = -1;
    userScoreTables.forEach(
      (scoreTable: UserScore) => {
        const partitionsSorted = this.processPartition(scoreTable);
        const bestPartition = ({id_partition: partitionsSorted[0][0], score_partition: partitionsSorted[0][1]} as UserScorePartition);
        const submissionProfile = scoreTable.user_partitions.submissions[bestPartition.id_partition];
        const bestSubmissionProfile = {partitions: this.processSubmissionProfile(submissionProfile)};
        const submissionProfileString = [];
        if (lastPartition !== bestPartition.id_partition && lastLowImpact !== bestSubmissionProfile.partitions.join()){
          submissionProfileString.push('(');
          bestSubmissionProfile.partitions.forEach(
            (profile) => {
              switch (profile.impact){
                case TypeOfJournal.LOW:
                  submissionProfileString.push('LOW-Impact');
                  break;
                case TypeOfJournal.LOW:
                  submissionProfileString.push('MEDIUM-Impact');
                  break;
                case TypeOfJournal.LOW:
                  submissionProfileString.push('HIGH-Impact');
                  break;
              }
              submissionProfileString.push(', ');
            }
          );
          submissionProfileString.pop();
          submissionProfileString.push(')');
          itemsTable.push({index: step, id_partition: bestPartition.id_partition, id_submission_profile: submissionProfileString.join('')});
          lastLowImpact = bestSubmissionProfile.partitions.join();
          lastPartition = bestPartition.id_partition;
        }
        step += 1;
      }
    );
    this.evolutionItems = itemsTable;
    console.log(this.evolutionItems);
  }



  subscribeTrainServiceEvolution(): void {
    this.trainServiceEvolutionSuscription = this.trainService.getScoreTableEvolution().subscribe(
      (response: Array<UserScore>) => {
        const lastScoreTable = response[response.length - 1];
        this.confusionMatrixDataFull = lastScoreTable.score_table;
        this.computeBasicStats();
        this.partitionsKey = lastScoreTable.user_partitions.partitions_keys;
        const partitionsSorted = this.processPartition(lastScoreTable);
        this.partition = ({id_partition: partitionsSorted[0][0], score_partition: partitionsSorted[0][1]} as UserScorePartition);
        const submissionProfile = lastScoreTable.user_partitions.submissions[this.partition.id_partition];
        this.submissionProfile = {partitions: this.processSubmissionProfile(submissionProfile)};
        this.processEvolution(response.reverse());

      }
    );
  }
}
