import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Article } from '@src/app/models/article-interface.model';
import { SnackMessageService } from '@src/app/services/snack-message.service';
import { TrainService } from '@src/app/services/train.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-train',
  templateUrl: './train.component.html',
  styleUrls: ['./train.component.css']
})
export class TrainComponent implements OnInit, OnDestroy {

  public currentArticle: Article | undefined;
  
  getLastArticleSuscription: Subscription | undefined;
  getArticleSuscription: Subscription | undefined;

  constructor(private trainService: TrainService,
              private router: Router,
              private snackMessageService: SnackMessageService) { }

  ngOnInit(): void {
    this.getLastArticle();
  }
  ngOnDestroy(): void {
    if (this.getLastArticleSuscription !== undefined){
      this.getLastArticleSuscription.unsubscribe();
    }
    if (this.getArticleSuscription !== undefined){
      this.getArticleSuscription.unsubscribe();
    }
  }

  getLastArticle(): void{
    this.getLastArticleSuscription = this.trainService.getLastArticle().subscribe(
      (article: Article) => {
          this.currentArticle = article;
      },
      error => {
        switch (error.status){
          case 403: // Not authorized.
            this.router.navigateByUrl('/');
            break;
          case 406: // Last article not found.
            this.getArticle();
            break;
          default:
            this.snackMessageService.notifyNewSnackMessage('We can\'t retrieve an article for you in this moment. Please come back later.');
            break;
        }
      }
    );
  }

  getArticle(): void{
    this.getArticleSuscription = this.trainService.getArticle().subscribe(
      (article: Article) => {
          this.currentArticle = article;
      }
    );
  }




}
