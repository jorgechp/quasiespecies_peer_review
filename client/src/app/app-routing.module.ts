import { AuthGuard } from '@src/app/guards/auth.guard';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { TrainComponent } from '@src/app/components/train/train.component';
import { StatsComponent } from '@src/app/components/stats/stats.component';
import { HelpComponent } from '@src/app/components/help/help.component';
import { AboutComponent } from '@src/app/components/about/about.component';
import { UserProfileComponent } from '@src/app/components/user-profile/user-profile.component';
import { WelcomeComponent } from '@src/app/components/welcome/welcome.component';
import { PrivacyComponent } from '@src/app/components/privacy/privacy.component';


const routes: Routes = [
  {path: '', component: WelcomeComponent},
  {path: 'train', component: TrainComponent, canActivate: [AuthGuard]},
  {path: 'stats', component: StatsComponent, canActivate: [AuthGuard]},
  {path: 'profile', component: UserProfileComponent, canActivate: [AuthGuard]},
  {path: 'help', component: HelpComponent},
  {path: 'about', component: AboutComponent},
  {path: 'privacy', component: PrivacyComponent},
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
