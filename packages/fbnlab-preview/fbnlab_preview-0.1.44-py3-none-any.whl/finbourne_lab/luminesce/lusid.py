import string
from math import ceil

import numpy as np

from finbourne_lab.luminesce.experiment import LumiExperiment
from finbourne_lab.luminesce.base import BaseLumiLab


class LusidLumiLab(BaseLumiLab):
    """The lusid lumi lab encapsulates standard measurements for lusid luminesce providers.

    """

    def __init__(self, atlas, verbose=False, skip_checks=False):
        """Creator for the LusidLumiLab class.

        Args:
            atlas (Atlas): the lumipy atlas to run luminesce queries with.
            verbose (bool): whether to run in verbose mode. This will give feedback on ensure (entity) steps
            during running. Defaults to false.
            skip_checks (bool): whether to skip ensure (instruments/portfolios/holdings/txns). Defaults to false.

        """

        required = [
            "lusid_portfolio",
            "lusid_instrument",
            "lusid_portfolio_holding",
            "lusid_portfolio_txn",
            "lab_testdata_lusid_holding",
            "lab_testdata_lusid_instrument",
            "lab_testdata_lusid_portfolio",
            "lab_testdata_lusid_transaction",
        ]

        missing = [r for r in required if not hasattr(atlas, r)]
        if len(missing) > 0:
            missing_str = '\n  '.join(missing)
            raise ValueError(f'Atlas is missing required providers:\n  {missing_str}')

        self.skip_checks = skip_checks
        super().__init__(atlas, verbose)

    def lusid_portfolio_read_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of lusid.portfolio

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 400].

        Returns:
            LumiExperiment: experiment object for the lusid.portfolio measurement.

        """
        rows_rng = kwargs.get('rows_rng', [1, 400])
        return self._reader_experiment('lusid_read_portfolio', self.atlas.lusid_portfolio, rows_rng, None)

    def lusid_instrument_read_measurement(self, **kwargs):
        """Make an experiment for measuring the performance of lusid.instrument

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].

        Returns:
            LumiExperiment: experiment object for the lusid.instrument measurement.

        """
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        return self._reader_experiment('lusid_read_instrument', self.atlas.lusid_instrument, rows_rng, None)

    def lusid_portfolio_txn_read_measurement(self, **kwargs):
        """Make a list of experiments for measuring the performance of lusid.portfolio.txn over different shape of data.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            force_ensure (bool): whether to force the ensure step. Defaults to False.
            txns_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of txns per portfolio. Defaults to 100, 1000, 10000.

        Notes:
            Data shape is the number of portfolios the txns are spread over. This is parameterised as the number of txns
            per portfolio in a scope. A test scope will be created for a given shape for each experiment.


        Returns:
            List[LumiExperiment]: experiment list for measuring txn read performance over different shaped data.

        """
        force_ensure = kwargs.get('force_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        rows_max = max(rows_rng)

        self._ensure_instruments(rows_max)

        txns_per_pf_set = kwargs.get('txns_per_pf', [10000, 1000, 100])

        experiments = []

        txn = self.atlas.lusid_portfolio_txn()

        for txns_per_pf in txns_per_pf_set:

            name = f'lusid_read_txn_{txns_per_pf}'
            scope = f'fbnlab_{name}'

            n_portfolios = ceil(rows_max/txns_per_pf)
            self._ensure_portfolios(n_portfolios, scope, force_ensure)
            self._ensure_txns(n_portfolios, txns_per_pf, scope, force_ensure)

            def build(x, s):
                return txn.select('*').where(txn.portfolio_scope == s).limit(x)

            ex = LumiExperiment(name, build, rows_rng, scope)
            experiments.append(ex)

        return experiments

    def lusid_portfolio_holding_read_measurement(self, **kwargs):
        """Make a list of experiments for measuring the performance of lusid.portfolio.holding over different shape of data.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            force_ensure (bool): whether to force the ensure step. Defaults to False.
            hlds_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of holdings per portfolio. Defaults to 100, 1000, 10000.

        Notes:
            Data shape is the number of portfolios the holdings are spread over. This is parameterised as the number of
            holdings per portfolio in a scope. A test scope will be created for a given shape for each experiment.


        Returns:
            List[LumiExperiment]: experiment list for measuring holdings read performance over different shaped data.

        """
        force_ensure = kwargs.get('force_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        rows_max = max(rows_rng)

        self._ensure_instruments(rows_max)

        hlds_per_pf_set = kwargs.get('hlds_per_pf', [10000, 1000, 100])

        experiments = []

        hld = self.atlas.lusid_portfolio_holding()

        for hlds_per_pf in hlds_per_pf_set:

            name = f'lusid_read_hld_{hlds_per_pf}'
            scope = f'fbnlab_{name}'

            n_portfolios = ceil(rows_max/hlds_per_pf)
            self._ensure_portfolios(n_portfolios, scope, force_ensure)
            self._ensure_holdings(n_portfolios, hlds_per_pf, scope, force_ensure)

            def build(x, s):
                return hld.select('*').where(hld.portfolio_scope == s).limit(x)

            ex = LumiExperiment(name, build, rows_rng, scope)
            experiments.append(ex)

        return experiments

    def lusid_instrument_writer_measurement(self, **kwargs):
        """Make a pair of experiments (one main, one baseline) for the instrument writer measurement.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 1000].

        Returns:
            List[LumiExperiment]: a pair of experiments for the measurement (main, base).

        """
        rows_rng = kwargs.get('rows_rng', [1, 1000])
        ins = self.atlas.lab_testdata_lusid_instrument()

        def baseline(x):
            tv = ins.select('*', Scope=self._make_write_scope('instrument')).limit(x).to_table_var()
            return tv.select('*').limit(1)

        def build(x):
            tv = ins.select('*', Scope=self._make_write_scope('instrument')).limit(x).to_table_var()
            writer = self.atlas.lusid_instrument_writer(to_write=tv)
            return writer.select('*')

        name = 'lusid_write_instrument'
        ex = LumiExperiment(name, build, rows_rng)
        base = LumiExperiment(name + '_base', baseline, rows_rng)
        return ex, base

    def lusid_portfolio_writer_measurement(self, **kwargs):
        """Make a pair of experiments (one main, one baseline) for the portfolio writer measurement.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 25].

        Returns:
            List[LumiExperiment]: a pair of experiments for the measurement (main, base).

        """
        rows_rng = kwargs.get('rows_rng', [1, 25])

        def baseline(x):
            pf_data = self.atlas.lab_testdata_lusid_portfolio(scope=self._make_write_scope('portfolio'))
            tv = pf_data.select('*').limit(x).to_table_var()
            return tv.select('*').limit(1)

        def build(x):
            pf_data = self.atlas.lab_testdata_lusid_portfolio(scope=self._make_write_scope('portfolio'))
            tv = pf_data.select('*').limit(x).to_table_var()
            writer = self.atlas.lusid_portfolio_writer(to_write=tv)
            return writer.select('*')

        name = 'lusid_write_portfolio'
        ex = LumiExperiment(name, build, rows_rng)
        base = LumiExperiment(name + '_base', baseline, rows_rng)
        return ex, base

    def lusid_portfolio_holding_writer_measurement(self, **kwargs):
        """Make a list of experiments for the portfolio holdings writer measurement over different data shapes.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

            Data shape is the number of portfolios the holdings are spread over. This is parameterised as the number of
            holdings per portfolio in a scope. A clean test scope will be created for a given shape for each write.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            force_ensure (bool): whether to force the ensure step. Defaults to False.
            hldg_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of holdings per portfolio. Defaults to 100, 1000, 10000.

        Returns:
            List[LumiExperiment]: a list of experiments containing the main and base for each data shape.

        """

        force_ensure = kwargs.get('force_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        hldg_per_pf_set = kwargs.get('hldg_per_pf_set', {100, 1000, 10000})

        experiments = []
        for hldg_per_pf in hldg_per_pf_set:

            def build(x, y):
                scope = self._make_write_scope('holding')
                n_portfolios = ceil(x/y)

                self._ensure_portfolios(n_portfolios, scope, force_ensure)
                self._ensure_instruments(y)

                tv = self.atlas.lab_testdata_lusid_holding(
                    scope=scope,
                    num_portfolios=n_portfolios,
                    instruments_per_portfolio=int(y),
                    effective_ats_per_instrument=1,
                    luids=self._luids_query(y).to_table_var()
                ).select('*').limit(x).to_table_var()

                writer = self.atlas.lusid_portfolio_holding_writer(to_write=tv)
                return writer.select('*')

            def baseline(x, y):
                tv = self.atlas.lab_testdata_lusid_holding(
                    scope=self._make_write_scope('holding'),
                    num_portfolios=ceil(x/y),
                    instruments_per_portfolio=int(y),
                    effective_ats_per_instrument=1,
                    luids=self._luids_query(y).to_table_var()
                ).select('*').limit(x).to_table_var()
                return tv.select('*').limit(1)

            name = f'lusid_write_holding_{hldg_per_pf}'
            ex = LumiExperiment(name, build, rows_rng, hldg_per_pf)
            experiments.append(ex)
            base = LumiExperiment(name + '_base', baseline, rows_rng, hldg_per_pf)
            experiments.append(base)

        return experiments

    def lusid_portfolio_txn_writer_measurement(self, **kwargs):
        """Make a list of experiments for the portfolio txns writer measurement over different data shapes.

        Notes:
            The baseline experiment measures the time to read out test data into a table var before going to the writer.
            The main step is the test data read + writer call. To measure the writer the baseline result should be
            subtracted from the main

            Data shape is the number of portfolios the txns are spread over. This is parameterised as the number of
            txns per portfolio in a scope. A clean test scope will be created for a given shape for each write.

        Keyword Args:
            rows_rng (Union[int, List[int]]): the range to sample when getting x-many rows. Given as a list containing
            two integers or a const int value. Defaults to [1, 10000].
            force_ensure (bool): whether to force the ensure step. Defaults to False.
            txns_per_pf_set (Set[int]): a set of integers that define the different data shapes to test for. Each value
            is the number of txns per portfolio. Defaults to 100, 1000, 10000.

        Returns:
            List[LumiExperiment]: a list of experiments containing the main and base for each data shape.

        """

        force_ensure = kwargs.get('force_ensure', False)
        rows_rng = kwargs.get('rows_rng', [1, 10000])
        txns_per_pf_set = kwargs.get('txns_per_pf_set', {100, 1000, 10000})

        experiments = []
        for txns_per_pf in txns_per_pf_set:
            def build(x, y):
                scope = self._make_write_scope('txn')
                n_portfolios = ceil(x/y)

                self._ensure_portfolios(n_portfolios, scope, force_ensure)
                self._ensure_instruments(y)

                tv = self.atlas.lab_testdata_lusid_transaction(
                    scope=scope,
                    num_portfolios=n_portfolios,
                    instruments_per_portfolio=int(y),
                    txns_per_instrument=1,
                    luids=self._luids_query(y).to_table_var()
                ).select('*').limit(x).to_table_var()

                writer = self.atlas.lusid_portfolio_txn_writer(to_write=tv)
                return writer.select('*')

            def baseline(x, y):
                tv = self.atlas.lab_testdata_lusid_transaction(
                    scope=self._make_write_scope('txn'),
                    num_portfolios=ceil(x/y),
                    instruments_per_portfolio=int(y),
                    txns_per_instrument=1,
                    luids=self._luids_query(y).to_table_var()
                ).select('*').limit(x).to_table_var()
                return tv.select('*').limit(1)

            name = f'lusid_write_txn_{txns_per_pf}'
            ex = LumiExperiment(name, build, rows_rng, txns_per_pf)
            experiments.append(ex)
            base = LumiExperiment(name + '_base', baseline, rows_rng, txns_per_pf)
            experiments.append(base)

        return experiments

    def _make_write_scope(self, label: str) -> str:
        letters = list(string.ascii_lowercase + string.digits)
        rand_id = ''.join(np.random.choice(letters, size=8))
        return f'fbnlab-{label}-writer-{rand_id}'

    def _luids_query(self, row_lim: int):
        inst = self.atlas.lusid_instrument()
        return inst.select(
            inst.lusid_instrument_id, inst.client_internal
        ).limit(row_lim)

    def _ensure_instruments(self, row_lim: int):
        if self.skip_checks:
            return

        self.log('Checking instruments', 2)
        inst_df = self._luids_query(row_lim).go(quiet=True)

        if inst_df.shape[0] >= row_lim:
            self.log('All present', 4)
            return

        self.log('Creating instruments', 2)
        tv = self.atlas.lab_testdata_lusid_instrument().select('*').limit(row_lim).to_table_var()
        self.atlas.lusid_instrument_writer(to_write=tv).select('^').limit(1).go(quiet=True)
        self.log('Done', 4)

    def _ensure_portfolios(self, n_portfolios: int, scope: str, force: bool):
        if self.skip_checks:
            return

        self.log(f'Checking portfolios in {scope}', 2)
        pf = self.atlas.lusid_portfolio()
        p_df = pf.select(pf.portfolio_scope).where(pf.portfolio_scope == scope).go(quiet=True)

        if p_df.shape[0] >= n_portfolios and not force:
            self.log('All present', 4)
            return

        self.log('Creating portfolios', 2)
        tv = self.atlas.lab_testdata_lusid_portfolio(
            scope=scope
        ).select('*').limit(n_portfolios).to_table_var()

        write = self.atlas.lusid_portfolio_writer(to_write=tv)
        write.select('^').limit(1).go(quiet=True)
        self.log('Done', 4)

    def _ensure_txns(self, n_portfolios: int, txns_per_pf: int, scope: str, force: bool):
        if self.skip_checks:
            return

        self.log(f'Checking txns in {scope}', 2)
        tx = self.atlas.lusid_portfolio_txn()
        t_df = tx.select(
            tx.portfolio_code
        ).where(
            tx.portfolio_scope == scope
        ).group_by(
            tx.portfolio_code
        ).agg(
            N=tx.portfolio_code.count()
        ).go(quiet=True)

        if t_df.shape[0] == n_portfolios and all(c == txns_per_pf for c in t_df['N']) and not force:
            self.log('All present', 4)
            return

        tv = self.atlas.lab_testdata_lusid_transaction(
            scope=scope,
            num_portfolios=n_portfolios,
            instruments_per_portfolio=txns_per_pf,
            txns_per_instrument=1,
            luids=self._luids_query(txns_per_pf).to_table_var()
        ).select('*').to_table_var()

        w = self.atlas.lusid_portfolio_txn_writer(to_write=tv)
        q = w.select(w.write_error_code, w.write_error_detail).where(w.write_error_code != 0)

        self.log(f'Creating txns', 2)
        df = q.go(quiet=True)
        if df.shape[0] > 0:
            err_msgs = '\n'.join(df.WriteErrorDetail.iloc[:5])
            raise ValueError(
                f'The txns write contained {df.shape[0]} errors:\n{err_msgs}'
            )
        self.log('Done', 4)

    def _ensure_holdings(self, n_portfolios: int, n_holdings: int, scope: str, force: bool):
        if self.skip_checks:
            return

        self.log(f'Checking holdings in {scope}', 2)
        hld = self.atlas.lusid_portfolio_holding()
        h_df = hld.select(
            hld.portfolio_code
        ).where(
            hld.portfolio_scope == scope
        ).group_by(
            hld.portfolio_code
        ).agg(
            N=hld.portfolio_code.count()
        ).go(quiet=True)

        if h_df.shape[0] == n_portfolios and all(c == n_holdings for c in h_df['N']) and not force:
            self.log('All present', 4)
            return

        tv = self.atlas.lab_testdata_lusid_holding(
            scope=scope,
            num_portfolios=n_portfolios,
            instruments_per_portfolio=n_holdings,
            effective_ats_per_instrument=1,
            luids=self._luids_query(n_holdings).to_table_var(),
        ).select('*').to_table_var()

        w = self.atlas.lusid_portfolio_holding_writer(to_write=tv)
        q = w.select(w.write_error_code, w.write_error_detail).where(w.write_error_code != 0)

        self.log('Creating holdings', 2)
        df = q.go(quiet=True)
        if df.shape[0] > 0:
            err_msgs = '\n'.join(df.WriteErrorDetail.iloc[:5])
            raise ValueError(
                f'The holdings write contained {df.shape[0]} errors:\n{err_msgs}'
            )
        self.log('Done', 4)
