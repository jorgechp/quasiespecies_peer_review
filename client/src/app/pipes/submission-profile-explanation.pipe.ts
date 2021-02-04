import { TypeOfJournal } from '@src/app/models/type-of-journal.enum';
import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'submissionProfileExplanation'
})
export class SubmissionProfileExplanationPipe implements PipeTransform {


responseMatrixFirstSubPartition = [
    'STATS.PARTITION_0_SUB_0',
    'STATS.PARTITION_1_SUB_0',
    'STATS.PARTITION_2_SUB_0',
    'STATS.PARTITION_3_SUB_0',
    'STATS.PARTITION_4_SUB_0',
    'STATS.PARTITION_5_SUB_0',
  ];
responseMatrixSecondSubPartition = [
    'STATS.PARTITION_0_SUB_1',
    'STATS.PARTITION_1_SUB_1',
    'STATS.PARTITION_2_SUB_1',
    'STATS.PARTITION_3_SUB_1',
    'STATS.PARTITION_4_SUB_1',
    'STATS.PARTITION_5_SUB_1',
    ];

responseMatrixThirdSubPartition = [
    'STATS.PARTITION_0_SUB_2',
    'STATS.PARTITION_1_SUB_2',
    'STATS.PARTITION_2_SUB_2',
    'STATS.PARTITION_3_SUB_2',
    'STATS.PARTITION_4_SUB_2',
    'STATS.PARTITION_5_SUB_2',
    ];

responseMatrix = [
  this.responseMatrixFirstSubPartition,
  this.responseMatrixSecondSubPartition,
  this.responseMatrixThirdSubPartition
];

transform(idSubPartition: number, args: number): string {
  const idPartition = args;
  return this.responseMatrix[idSubPartition][idPartition];
}



}
