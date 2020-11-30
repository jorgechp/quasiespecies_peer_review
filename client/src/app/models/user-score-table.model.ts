export interface UserScoreTable{
    LOW: UserScoreRow;
    MEDIUM: UserScoreRow;
    HIGH: UserScoreRow;
}

interface UserScoreRow{
    LOW: number;
    MEDIUM: number;
    HIGH: number;
}