import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Article } from '@src/app/models/article-interface.model';
import { AnswerResult } from '@src/app/models/answer-result-model';
import { UserScore } from '@src/app/models/user-score.model';

const EVOLUTION_ROWS_PER_STEP = 15;

@Injectable({
  providedIn: 'root'
})
export class TrainService {
  private getArticleUrl = 'http://localhost:7000/train/article';
  private getLastArticleUrl = 'http://localhost:7000/train/article/last';
  private userAnswerUrl = 'http://localhost:7000/train/article';
  private userScoreTableUrl = 'http://localhost:7000/train/score/table';
  private userScoreTableEvolutionUrl = 'http://localhost:7000/train/score/table/' + EVOLUTION_ROWS_PER_STEP;

  constructor(private httpClient: HttpClient) { }

  getArticle(): Observable<Article> {
    return this.httpClient.get<Article>(this.getArticleUrl, { withCredentials: true });
  }

  getLastArticle(): Observable<Article>{
    return this.httpClient.get<Article>(this.getLastArticleUrl, { withCredentials: true });
  }

  getScoreTable(): Observable<Array<UserScore>>{
    return this.httpClient.get<Array<UserScore>>(this.userScoreTableUrl, { withCredentials: true });
  }

  getScoreTableEvolution(): Observable<Array<UserScore>>{
    return this.httpClient.get<Array<UserScore>>(this.userScoreTableEvolutionUrl, { withCredentials: true });
  }

  answer(response: string): Observable<AnswerResult>{
    const answer = {impact: response};
    return this.httpClient.post<AnswerResult>(this.userAnswerUrl, JSON.stringify(answer), { withCredentials: true });
  }

}
