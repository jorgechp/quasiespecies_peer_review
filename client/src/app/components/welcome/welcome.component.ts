import { Component, OnInit, OnDestroy } from '@angular/core';
import { UserService } from '@src/app/services/user.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-welcome',
  templateUrl: './welcome.component.html',
  styleUrls: ['./welcome.component.css']
})
export class WelcomeComponent implements OnInit, OnDestroy {

  isLogged = false;
  loginSuscription: Subscription | undefined;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.subscribeLogin();
  }

  ngOnDestroy(): void {
    if (this.loginSuscription !== undefined){
      this.loginSuscription.unsubscribe();
    }
  }

  subscribeLogin(): void{
    this.loginSuscription = this.userService.checkLogin().subscribe(
      (isLogged: boolean) => {
        this.isLogged = isLogged;
      }
    );
  }

}