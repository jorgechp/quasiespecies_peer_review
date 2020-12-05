import { TypeOfJournal } from '@src/app/models/type-of-journal.enum';

export interface SubmissionProfileInterface{
    partitions: SubmissionProfileSubPartition[];
}

export interface SubmissionProfileSubPartition{
    impact: TypeOfJournal;
    score: number;
}