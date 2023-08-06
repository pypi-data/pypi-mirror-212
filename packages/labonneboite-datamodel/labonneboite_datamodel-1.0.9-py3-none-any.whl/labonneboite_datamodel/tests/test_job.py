from unittest import TestCase
from .. import Naf, Job


class TestJob(TestCase):

    def _get_valid_job(self) -> dict:
        return {
            "rome": "M1234",
            "naf": "12",
            "label_naf": "Something",
            "label_rome": "Something",
            "hirings": 60

        }

    def _get_valid_naf(self) -> dict:
        return {
            "naf": "1234Z",
            "label": "Something",
        }

    # valid job
    def test_job_valid(self) -> None:
        data = self._get_valid_job()
        self.assertTrue(Job.validate(data).rome == "M1234")

    def test_naf_valid(self) -> None:
        data = self._get_valid_naf()
        self.assertTrue(Naf.validate(data).naf == "1234Z")

    # invalid naf

    def test_job_naf_invalid(self) -> None:
        data = self._get_valid_job()

        for value in ["1f", "0", "abc2"]:

            data["naf"] = value

            with self.assertRaises(ValueError):
                Job.validate(data)

    def test_naf_naf_invalid(self) -> None:
        data = self._get_valid_naf()

        for value in ["1f", "0", "abc2", "123f5", "f2345"]:

            data["naf"] = value

            with self.assertRaises(ValueError):
                Naf.validate(data)

    # invalid naf

    def test_job_rome_invalid(self) -> None:
        data = self._get_valid_job()

        for value in ["1".zfill(5), "0".zfill(4), "abc2".zfill(5)]:

            data["rome"] = value

            with self.assertRaises(ValueError):
                Job.validate(data)
