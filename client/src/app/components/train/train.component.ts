import { TranslateService } from '@ngx-translate/core';
import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AnswerResult } from '@src/app/models/answer-result-model';
import { Article } from '@src/app/models/article-interface.model';
import { SnackMessageService } from '@src/app/services/snack-message.service';
import { TrainService } from '@src/app/services/train.service';
import { UserService } from '@src/app/services/user.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-train',
  templateUrl: './train.component.html',
  styleUrls: ['./train.component.css']
})
export class TrainComponent implements OnInit, OnDestroy {

  public static SNACK_SERVICE_TRAIN_NOTIFICATION_TIME = 5000;

  public currentArticle: Article | undefined;
  public isButtonsDisabled = false;
  public numberOfAnswers = 0;

  isLogged = false;

  getLastArticleSuscription: Subscription | undefined;
  getArticleSuscription: Subscription | undefined;
  userAnswerSuscription: Subscription | undefined;
  loginSuscription: Subscription | undefined;
  snackMessageSubscription: Subscription | undefined;
  numberOfUserAnswersSuscription: Subscription | undefined;

  constructor(private trainService: TrainService,
              private router: Router,
              private translateService: TranslateService,
              private userService: UserService,
              private snackMessageService: SnackMessageService) { }

  ngOnInit(): void {
    this.subscribeCheckLogin();
    this.snackMessageService.notifyDismiss();
    this.getNumberOfUserAnswers();
  }

  ngOnDestroy(): void {
    if (this.getLastArticleSuscription !== undefined){
      this.getLastArticleSuscription.unsubscribe();
    }
    if (this.getArticleSuscription !== undefined){
      this.getArticleSuscription.unsubscribe();
    }
    if (this.userAnswerSuscription !== undefined){
      this.userAnswerSuscription.unsubscribe();
    }
    if (this.loginSuscription !== undefined){
      this.loginSuscription.unsubscribe();
    }
    if (this.snackMessageSubscription !== undefined){
      this.snackMessageSubscription.unsubscribe();
    }
    if (this.numberOfUserAnswersSuscription !== undefined){
      this.numberOfUserAnswersSuscription.unsubscribe();
    }
  }

  subscribeCheckLogin(): void{
    this.loginSuscription = this.userService.checkLogin().subscribe(
      (isLogged: boolean) => {
        if (isLogged){
          this.getLastArticle();
        }
        this.isLogged = isLogged;
      }
    );
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
            this.snackMessageService.notifyNewSnackMessage(this.translateService.instant('SNACK.TRAIN_ERROR_RETRIEVING_ARTICLES'));
            break;
        }
      }
    );
  }

  getArticle(): void{
    this.getArticleSuscription = this.trainService.getArticle().subscribe(
      (article: Article) => {
          this.currentArticle = article;
          this.getArticleSuscription?.unsubscribe();
      },
      error => {
        switch (error.status){
          case 403: // Not authorized.
            this.router.navigateByUrl('/');
            break;
          default:
            this.snackMessageService.notifyNewSnackMessage(this.translateService.instant('SNACK.TRAIN_ERROR_RETRIEVING_ARTICLES'));
            break;
      }
    }
    );
  }

  getNumberOfUserAnswers(): void{
    this.numberOfUserAnswersSuscription = this.trainService.getNumberOfUserAnswers().subscribe(
      (numberOfAnswers: number ) => {
        this.numberOfAnswers = numberOfAnswers;
        this.numberOfUserAnswersSuscription?.unsubscribe();
      }
    );
  }

  doArticleAnswer(response: string): void{
    this.isButtonsDisabled = true;
    if (response !== undefined){
      this.userAnswerSuscription = this.trainService.answer(response).subscribe(
        (answer: AnswerResult) => {
          this.numberOfAnswers = answer.total_answers;
          if (answer.user_score === 1){
            this.snackMessageService.notifyNewSnackMessage(this.translateService.instant('SNACK.TRAIN_OK_SCORE_1') + ' '
                                                            + response + this.translateService.instant('SNACK.TRAIN_OK_SCORE_2')
                                                            , TrainComponent.SNACK_SERVICE_TRAIN_NOTIFICATION_TIME);
          }else{
            this.snackMessageService.notifyNewSnackMessage(this.translateService.instant('SNACK.TRAIN_ERROR_SCORE_1')
                                                            + ' ' + answer.real_journal_quality
                                                            + this.translateService.instant('SNACK.TRAIN_ERROR_SCORE_2')
                                                            , TrainComponent.SNACK_SERVICE_TRAIN_NOTIFICATION_TIME);
          }
          this.snackMessageSubscription = this.snackMessageService.subscribeDissmising().subscribe(
            () => { this.snackMessageSubscription?.unsubscribe(); this.getArticle(); this.isButtonsDisabled = false; }
          );
        }
      );
    }

  }

}
