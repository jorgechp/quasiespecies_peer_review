import { NgModule, NO_ERRORS_SCHEMA } from '@angular/core';
import { NativeScriptModule } from '@nativescript/angular';

import { AppRoutingModule } from '@src/app/app-routing.module.tns';
import { AppComponent } from '@src/app/app.component';
import { AutoGeneratedComponent } from '@src/app/auto-generated/auto-generated.component';
import { HeaderComponent } from '@src/app/components/header/header/header.component';
import { ContentContainerComponent } from '@src/app/components/content-container/content-container.component';
import { FooterComponent } from '@src/app/components/footer/footer.component';
import { TrainComponent } from '@src/app/components/train/train.component';
import { StatsComponent } from '@src/app/components/stats/stats.component';
import { HelpComponent } from '@src/app/components/help/help.component';
import { AboutComponent } from '@src/app/components/about/about.component';
import { SignupComponent } from '@src/app/components/signup/signup.component';
import { WelcomeComponent } from '@src/app/components/welcome/welcome.component';
import { InfoMessageComponent } from '@src/app/components/info-message/info-message.component';
import { ConfussionMatrixComponent } from '@src/app/components/stats/confusion-matrix/node_modules/@src/app/app/stats/confussion-matrix/confussion-matrix.component';
import { PrivacyComponent } from '@src/app/components/privacy/privacy.component';


// Uncomment and add to NgModule imports if you need to use two-way binding and/or HTTP wrapper
// import { NativeScriptFormsModule, NativeScriptHttpClientModule } from '@nativescript/angular';

@NgModule({
  declarations: [
    AppComponent,
    AutoGeneratedComponent,
    HeaderComponent,
    ContentContainerComponent,
    FooterComponent,
    TrainComponent,
    StatsComponent,
    HelpComponent,
    AboutComponent,
    SignupComponent,
    WelcomeComponent,
    InfoMessageComponent,
    ConfussionMatrixComponent,
    PrivacyComponent,
  ],
  imports: [
    NativeScriptModule,
    AppRoutingModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
  schemas: [NO_ERRORS_SCHEMA]
})
/*
Pass your application module to the bootstrapModule function located in main.ts to start your app
*/
export class AppModule { }
