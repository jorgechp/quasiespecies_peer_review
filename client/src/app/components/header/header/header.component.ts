import { Component, OnInit, OnDestroy } from '@angular/core';
import { UserService } from '@src/app/services/user.service';
import { Subscription } from 'rxjs';
import {Router} from '@angular/router';
import { SnackMessageService } from '@src/app/services/snack-message.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit, OnDestroy {

  logoutSuscription: Subscription | undefined;

  constructor(private router: Router,
              private snackMessageService: SnackMessageService,
              private userService: UserService) { }

  ngOnInit(): void {
  }

  ngOnDestroy(): void {
    if (this.logoutSuscription !== undefined){
      this.logoutSuscription.unsubscribe();
    }
  }

  doLogout(): void{
    this.logoutSuscription = this.userService.logout().subscribe(
      (response: boolean) => {
        console.log('Logout');
        this.snackMessageService.notifyNewSnackMessage('See you soon!');
        this.router.navigateByUrl('/');
      }
    );
  }

}
