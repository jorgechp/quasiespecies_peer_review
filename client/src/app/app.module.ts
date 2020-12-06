import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule, HTTP_INTERCEPTORS  } from '@angular/common/http';

import { AppRoutingModule } from '@src/app/app-routing.module';
import { AppComponent } from '@src/app/app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AutoGeneratedComponent } from '@src/app/auto-generated/auto-generated.component';
import { HeaderComponent } from '@src/app/components/header/header/header.component';

import {NgcCookieConsentConfig, NgcCookieConsentModule} from 'ngx-cookieconsent';

// import { AppMaterialModule } from '@src/app/app-material/app-material.module';

import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import {MatButtonModule} from '@angular/material/button';
import {MatIconModule} from '@angular/material/icon';
import {MatToolbarModule} from '@angular/material/toolbar';
import {MatFormFieldModule} from '@angular/material/form-field';
import {MatInputModule} from '@angular/material/input';
import {MatSnackBarModule} from '@angular/material/snack-bar';
import {MatTableModule} from '@angular/material/table';
import {MatCheckboxModule} from '@angular/material/checkbox';

import { FooterComponent } from '@src/app/components/footer/footer.component';
import { TrainComponent } from '@src/app/components/train/train.component';
import { StatsComponent } from '@src/app/components/stats/stats.component';
import { HelpComponent } from '@src/app/components/help/help.component';
import { AboutComponent } from '@src/app/components/about/about.component';
import { SignupComponent } from '@src/app/components/signup/signup.component';
import { WelcomeComponent } from '@src/app/components/welcome/welcome.component';
import { InterceptorHttp } from '@src/app/interceptors/http-interceptor';
import { KeywordsPipe } from '@src/app/pipes/keywords.pipe';
import { ConfusionMatrixComponent } from '@src/app/components/stats/confusion-matrix/confusion-matrix.component';
import { PrivacyComponent } from '@src/app/components/privacy/privacy.component';

const cookieConfig:NgcCookieConsentConfig = {
  cookie: {
    domain: 'localhost' // or 'your.domain.com' // it is mandatory to set a domain, for cookies to work properly (see https://goo.gl/S2Hy2A)
  },
  palette: {
    popup: {
      background: '#36363A'
    },
    button: {
      background: '#F6F7F8',
    }
  },
  theme: 'edgeless',
  type: 'opt-out'
};

@NgModule({
  declarations: [
    AppComponent,
    AutoGeneratedComponent,
    HeaderComponent,
    FooterComponent,
    TrainComponent,
    StatsComponent,
    HelpComponent,
    AboutComponent,
    SignupComponent,
    WelcomeComponent,
    KeywordsPipe,
    ConfusionMatrixComponent,
    PrivacyComponent
  ],
  exports: [
    HeaderComponent
  ],
  imports: [
    NgcCookieConsentModule.forRoot(cookieConfig),
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule,
    // AppMaterialModule,
    MatButtonModule,
    MatIconModule,
    MatToolbarModule,
    MatFormFieldModule,
    MatInputModule,
    MatSnackBarModule,
    MatTableModule,
    MatCheckboxModule
  ],
  providers: [ {provide: HTTP_INTERCEPTORS , useClass: InterceptorHttp, multi: true}],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA]
})
export class AppModule { }
