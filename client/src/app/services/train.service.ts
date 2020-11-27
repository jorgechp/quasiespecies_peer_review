import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Article } from '@src/app/models/article-interface.model';

@Injectable({
  providedIn: 'root'
})
export class TrainService {
  private getArticleUrl = 'http://localhost:7000/train/article';
  private getLastArticleUrl = 'http://localhost:7000/train/article/last';

  constructor(private httpClient: HttpClient) { }

  getArticle(): Observable<Article> {
    return this.httpClient.get<Article>(this.getArticleUrl, { withCredentials: true });
  }

  getLastArticle(): Observable<Article>{
    return this.httpClient.get<Article>(this.getLastArticleUrl, { withCredentials: true });
  }
}
