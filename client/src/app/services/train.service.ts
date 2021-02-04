import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Article } from '@src/app/models/article-interface.model';
import { AnswerResult } from '@src/app/models/answer-result-model';
import { UserScore } from '@src/app/models/user-score.model';
import { CONFIG } from '@src/app/config';

const EVOLUTION_ROWS_PER_STEP = 30;

@Injectable({
  providedIn: 'root'
})
export class TrainService {

  private getArticleUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/train/article';
  private getLastArticleUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/train/article/last';
  private userAnswerUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/train/article';
  private userScoreTableUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/train/score/table';
  private userNumberOfAnswers = CONFIG.HOST + ':' + CONFIG.PORT + '/train/score/times';
  private userScoreTableEvolutionUrl = CONFIG.HOST + ':' + CONFIG.PORT + '/train/score/table/' + EVOLUTION_ROWS_PER_STEP;

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

  answer(response: string, totalResponseTime: number): Observable<AnswerResult>{
    const answer = {impact: response, time: totalResponseTime};
    return this.httpClient.post<AnswerResult>(this.userAnswerUrl, JSON.stringify(answer), { withCredentials: true });
  }

  getNumberOfUserAnswers(): Observable<number> {
    return this.httpClient.get<number>(this.userNumberOfAnswers, { withCredentials: true });
  }

}
