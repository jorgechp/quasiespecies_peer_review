import { TestBed } from '@angular/core/testing';

import { RecaptchaValidationService } from './recaptcha-validation.service';

describe('RecaptchaValidationService', () => {
  let service: RecaptchaValidationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RecaptchaValidationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
