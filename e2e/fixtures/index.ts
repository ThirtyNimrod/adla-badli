import path from 'path';

export const TEST_DATA_DIR = path.join(__dirname, '..', 'test-data');

export const FIXTURES = {
  md: path.join(TEST_DATA_DIR, 'sample.md'),
  csv: path.join(TEST_DATA_DIR, 'sample.csv'),
  svg: path.join(TEST_DATA_DIR, 'sample.svg'),
};
