Engine tests (no GUI, no cloud — uses a throwaway local database):

    PYTHONPATH=tests/stubs python3 tests/test_engine.py <empty-temp-folder> <folder-with-a-copy-of-ALLOCATE_PRO.py>

Use a folder that does NOT contain allocate_pro_cloud_token.txt, so the test
can never reach the real cloud database (the test checks this and stops).
