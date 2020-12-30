import { TestBed } from '@angular/core/testing';

import { SnackMessageService } from '@src/app/services/snack-message.service';

describe('SnackMessageService', () => {
  let service: SnackMessageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SnackMessageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
