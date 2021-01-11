import { TypeOfJournal } from '@src/app/models/type-of-journal.enum';
export interface UserScore{
    score_table: UserScoreTable;
    user_partitions: UserScorePartitions;
}

export interface UserScoreTable{
    LOW: UserScoreRow;
    MEDIUM: UserScoreRow;
    HIGH: UserScoreRow;
}

export interface UserScoreRow{
    LOW: number;
    MEDIUM: number;
    HIGH: number;
}

export interface UserScorePartitions{
    partitions: {[idPartition: number]: number};
    partitions_keys: [];
    submissions: [];
}

export interface UserScorePartition{
    id_partition: number;
    score_partition: number;
}

export interface UserScoreProfile{
    0: Array<TypeOfJournal>;
    1: number;
}
