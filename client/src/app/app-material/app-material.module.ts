import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import {MatToolbarModule} from '@angular/material/toolbar';
import {MatIconModule} from '@angular/material/icon'; 

@NgModule({
  declarations: [],
  exports: [
    MatToolbarModule,
    MatIconModule
  ],
  imports: [
    CommonModule
  ]
})
export class AppMaterialModule { }
