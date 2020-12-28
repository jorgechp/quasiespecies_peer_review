import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, RouterStateSnapshot, CanActivate } from '@angular/router';
import { Observable } from 'rxjs';
import { UserService } from '@src/app/services/user.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(private userService: UserService){}

  canActivate(
    childRoute: ActivatedRouteSnapshot, state: RouterStateSnapshot): Observable<boolean>{
      return this.userService.checkLogin();
  }
}
