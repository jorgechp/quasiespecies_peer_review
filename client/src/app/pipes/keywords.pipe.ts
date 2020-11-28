import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'keywordsPipe'
})
export class KeywordsPipe implements PipeTransform {

  transform(keywords: string): string {
    return keywords.split(';').join('; ').toLowerCase();
  }

}
