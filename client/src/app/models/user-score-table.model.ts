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