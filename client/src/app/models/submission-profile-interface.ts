import { TypeOfJournal } from '@src/app/models/type-of-journal.enum';

export interface SubmissionProfileInterface{
    LOW: Array<TypeOfJournal>;
    MEDIUM: Array<TypeOfJournal>;
    HIGH: Array<TypeOfJournal>;
}
