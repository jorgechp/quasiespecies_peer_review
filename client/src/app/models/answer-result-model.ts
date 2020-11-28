import { TypeOfJournal } from '@src/app/models/type-of-journal.enum';

export interface AnswerResult{
    real_journal_quality: number;
    user_journal_quality: number;
    user_score: number;
}
